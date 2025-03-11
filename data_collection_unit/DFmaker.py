"""
Author: Navjot Saroa

Collects telemetry data from the F1 game and stores as a dataframe. Can be exported as a CSV or a 
parquet file.
"""

import pandas as pd
from UDP import *
import traceback
import copy
import datetime

class LiveDFMaker():
    def __init__(self, required_packets = [2, 6], required_columns = ["Speed", "Throttle", "Brake", "nGear", "Distance"]):
        # UDP stuff
        self.UDP_conn = self.get_udp_session()
        self.sock = self.UDP_conn.start_session()
        self.dataframe = pd.DataFrame(columns = required_columns)
        self.LAP_DATA_PACK = 2
        self.CAR_TELEMETRY_PACK = 6
        self.GAME_VERSION = None # F1 2019 to F1 24 is valid for telemetry analysis.
        self.SESSION_UID = None  # Dataframe will be made for individual sessions
        self.SESSION_TIME = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        self.required_packets = required_packets    # Default is [2, 6], which is the LAP_DATA_PACK and the CAR_TELEMETRY_PACK
        self.packet_names = [
            self.UDP_conn.packet_type[packet_id].__name__
            for packet_id in self.required_packets
        ]

    def get_udp_session(self):
        """
        Initiates a UDP session (logical packet exchange).

        Args:
            - None
        
        Returns:
            - UDP_session (UDP): Custom object, will be used to initialise a UDP session.
        """

        UDP_IP = input("Enter IP address: ")  # Replace with your own IP address in str format
        UDP_PORT = int(input("Enter port: "))     # Replace with your own port in int format
        UDP_session = UDP(UDP_IP, UDP_PORT)
        return UDP_session

    def collect_packets(self):
        """
        Collects the data packets sent by the game and picks out the ones that are useful.
        Then it processes and stores the required data in a pandas dataframe
        
        Args:
            None

        Returns:
            None
        """

        try:
            print("Retrieving Initialising Data...")
            # Receive and handle incoming UDP data packets
            data, addr = self.UDP_conn.receive(2048, self.sock)   # Gets the data packet from the game, packet has not been handled yet, just so happens that its header can be accessed without that
            packet_id = data.m_packetId

            if not (self.GAME_VERSION or self.SESSION_UID):   # Set up file naming data
                self.GAME_VERSION = data.m_packetFormat
                self.SESSION_UID = data.m_sessionUID
                DRIVER_ID = data.m_playerCarIndex
            print("Initialising Data Retrieved.")

            while packet_id not in self.required_packets:   # Keep collecting data and discarding until actual relevant data is received
                data, addr = self.UDP_conn.receive(2048, self.sock) 
                packet_id = data.m_packetId

            if packet_id in self.required_packets:
                handled_packet = self.UDP_conn.handle_packet(addr, self.UDP_conn.packet_type[packet_id])

                while handled_packet.m_header.m_packetId != self.LAP_DATA_PACK:
                    pass    # Wait for packet_id = 2 to show up
                
                # First we need to wait for the actual flying lap to begin
                # This block is not just in the while loop above (with if instead of while) because we always need prev_lap_num and this way we don't have to worry about race conditions.
                print("Awaiting Telemetry Data Stream")
                prev_lap_num = self.wait_for_flying_lap(handled_packet, DRIVER_ID)
                print("Collecting Telemetry...")
                
                # Start data collection
                self.data_collection_unit(prev_lap_num, DRIVER_ID)

        except Exception as e:
            print(f"Error in collect_packets: {e}")    
            traceback.print_exc()

        return

    def wait_for_flying_lap(self, handled_packet, driver_id):
        """
        Waits for a flying lap to start so that collect_packets can proceed to collect data.
        Start of flying lap is detected when car is first within 5 metres of start line (Lap distance is
        negative if first lap of the session, and is greater than 5 if lap count for the session
        is greater than 0 before the start of the lap user wants to track)

        Args:
            - handled_packet (byte stream): First packet to initiate checks for the infinite waiting loop.
            - driver_id (int): ID of user, found in packet headers.

        Returns:
            - initial_lap_number (int): Will be used to compare to current lap to detect change, indiating end of lap.
        """

        lap_distance = handled_packet.m_lapData[driver_id].m_lapDistance
        car_has_not_crossed_start = lap_distance < 0 or lap_distance > 5    # Car's distance from start line is not between 0m and 5m

        while car_has_not_crossed_start:
            data, addr = self.UDP_conn.receive(2048, self.sock)
            packet_id = data.m_packetId
            if packet_id == self.LAP_DATA_PACK:
                handled_packet = self.UDP_conn.handle_packet(addr, self.UDP_conn.packet_type[packet_id])        
                lap_distance = handled_packet.m_lapData[driver_id].m_lapDistance
                car_has_not_crossed_start = lap_distance < 0 or lap_distance > 5

        initial_lap_number = handled_packet.m_lapData[driver_id].m_currentLapNum
        return initial_lap_number
    
    def data_collection_unit(self, prev_lap_num, driver_id):
        """
        Infinite loop of data collection, processing, and storage until lap is completed.

        Args:
            - prev_lap_num (int): Used to compare to current lap number. Change indicated end of lap.
            - driver_id (int): ID of user, found in packet headers.

        Returns:
            None
        """

        try:
            EMPTY_BUFFER = {    # m_overallFrameIdentifier is always greater than 0, so -1 means no frame has been recorded yet
                "lap_data" : (None, -1),
                "car_telemetry": (None, -1)
            }

            buffer_dict = copy.deepcopy(EMPTY_BUFFER)   # Just holds the unextracted data packet sent from game

            while True:
                data, addr = self.UDP_conn.receive(2048, self.sock)
                packet_id = data.m_packetId

                if packet_id == self.LAP_DATA_PACK:
                    handled_packet = self.UDP_conn.handle_packet(addr, self.UDP_conn.packet_type[packet_id])
                    curr_lap_number = handled_packet.m_lapData[driver_id].m_currentLapNum
                    
                    # Note that m_driverStatus could be used if the time was not collected from Time Trial.
                    # Since data analysis is done with pro driver qualifying laps, we just assumed
                    # data would be collected from time trial since the car is in optimal conditions
                    # in time trial, like in real life qualifying.
                    lap_ended = prev_lap_num != curr_lap_number
                    if lap_ended:
                        break

                    buffer_dict["lap_data"] = (handled_packet, data.m_overallFrameIdentifier)

                if packet_id == self.CAR_TELEMETRY_PACK:
                    handled_packet = self.UDP_conn.handle_packet(addr, self.UDP_conn.packet_type[packet_id])
                    buffer_dict["car_telemetry"] = (handled_packet, data.m_overallFrameIdentifier)

                if self.buffer_ready_to_append(buffer_dict):
                    extracted_data = self.extract_data(buffer_dict, driver_id)
                    new_row = pd.DataFrame.from_dict([extracted_data])
                    self.dataframe = pd.concat([self.dataframe, new_row], ignore_index = True)
                    buffer_dict = copy.deepcopy(EMPTY_BUFFER)

        except Exception as e:
            print(f"Error in collect_packets: {e}")    
            traceback.print_exc()

        return
    
    def buffer_ready_to_append(self, buffer):
        """
        Checks if buffer of packets is ready to be processed, with extracted data being added to 
        dataframe.

        Args:
            - buffer (dict): Dictionary of bytes representing the packets collected.

        Returns:
            - buffer_ready (bool): Buffer has both packets ready, and frames match, indicating the packets are from the same point in lap.
        """
        
        packet2, frame2 = buffer["lap_data"]
        packet6, frame6 = buffer["car_telemetry"]

        both_packets_exist = packet2 and packet6
        frames_match = (frame2 == frame6)

        buffer_ready = both_packets_exist and frames_match

        return buffer_ready
    
    def extract_data(self, buffer, driver_id):
        """
        Extracts data from the buffer, preparing it for appending to the dataframe.

        Args:
            - buffer (dict): Dictionary of bytes representing the packets collected.
            - driver_id (int): ID of user, found in packet headers.

        Returns:
            - extracted_data (dict): Dictionary of relevant data, formatted specifically to facilitate appending to dataframe.
        """

        m_lapDistance = buffer["lap_data"][0].m_lapData[driver_id].m_lapDistance
        m_speed = buffer["car_telemetry"][0].m_carTelemetryData[driver_id].m_speed
        m_throttle = round(buffer["car_telemetry"][0].m_carTelemetryData[driver_id].m_throttle, 5)
        m_brake = round(buffer["car_telemetry"][0].m_carTelemetryData[driver_id].m_brake, 5)
        m_gear = buffer["car_telemetry"][0].m_carTelemetryData[driver_id].m_gear

        extracted_data = {
            "Distance" : m_lapDistance,
            "Speed": m_speed,
            "Throttle" : m_throttle,
            "Brake" : m_brake,
            "nGear" : m_gear
        }

        return extracted_data
    
    def scale_dataframe_down(self, scale_factor):
        """
        Scales dataframe to 1/scale_factor it's original size. This is because the telemetry data
        collected from the game is significantly larger than the real-life professional driver data.
        The scaling is done by taking each scale_factor-th row of the dataframe. This maintains the
        general trend of the data since it is a time series.

        Args:
            - scale_factor (int): Scale to reduce the dataframe by.
        
        Returns:
            Scaled down version of self.dataframe.
        """

        self.dataframe = self.dataframe[::scale_factor]

        return
    
    def export_dataframe(self):
        """
        Exports the dataframe in JSON format.

        Args:
            None
        
        Returns:
            JSON files for the dataframe.
        """
        
        print("Exporting Dataframe...")
        self.dataframe.to_json(f"data_collection_unit/{self.GAME_VERSION}_{self.SESSION_UID}_{self.SESSION_TIME}.json")
        print("Dataframe Exported")

if __name__ == "__main__":
    DF = LiveDFMaker()
    DF.collect_packets()
    DF.scale_dataframe_down(20)
    DF.export_dataframe()

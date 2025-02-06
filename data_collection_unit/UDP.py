import socket
import ctypes as ct
from structures import *

class UDP():
    packet_type = {
        0: PacketMotionData,                # Motion
        1: PacketSessionData,               # Session
        2: PacketLapData,                   # Lap Data
        3: PacketEventData,                 # Event
        4: PacketParticipantsData,          # Participants
        5: PacketCarSetupData,              # Car Setups
        6: PacketCarTelemetryData,          # Car Telemetry
        7: PacketCarStatusData,             # Car Status
        8: PacketFinalClassificationData,   # Final Classification
        9: PacketLobbyInfoData,             # Lobby Info
        10: PacketCarDamageData,            # Car Damage
        11: PacketSessionHistoryData,       # Session History
        12: PacketTyreSetsData,             # Tyre Sets
        13: PacketMotionExData              # Motion Ex
    }

    event_codes = {
        "SSTA": None,                       # Session Started
        "SEND": None,                       # Session Ended
        "FTLP": FastestLap,                 # Fastest Lap
        "RTMT": Retirement,                 # Retirement
        "DRSE": None,                       # DRS enabled
        "DRSD": None,                       # DRS disabled
        "TMPT": TeamMateInPits,             # Team mate in pits
        "CHQF": None,                       # Chequered flag
        "RCWN": RaceWinner,                 # Race Winner
        "PENA": Penalty,                    # Penalty Issued
        "SPTP": SpeedTrap,                  # Speed Trap Triggered
        "STLG": StartLights,                # Start lights
        "LGOT": None,                       # Lights out
        "DTSV": DriveThroughPenaltyServed,  # Drive through served
        "SGSV": StopGoPenaltyServed,        # Stop go served
        "FLBK": Flashback,                  # Flashback
        "BUTN": Buttons,                    # Button status
        "RDFL": None,                       # Red Flag
        "OVTK": Overtake                    # Overtake
    }

    def __init__(self, UDP_IP, UDP_PORT):
        self.UDP_IP = UDP_IP
        self.UDP_PORT = UDP_PORT


    def start_session(self):
        """
        return: Socket sock
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.UDP_IP, self.UDP_PORT))
        print(f"Session Initiated! IP: {self.UDP_IP}; Port: {self.UDP_PORT}")
        return sock

    def parse_packet_header(self, data):
        """
        param1: byte* data; array of bytes
        return: byte* header; information about the packet being received
        """
        header = PacketHeader.from_buffer_copy(data[:ct.sizeof(PacketHeader)])
        return header

    def handle_packet(self, data, packet):
        """
        Will handle different packet types based on m_packetId
        param1: byte* data; array of bytes
        param2: byte* packet; received from F1 23
        return: byte* info; will still include the header data
        """
        info = packet.from_buffer_copy(data)
        return info

    def receive(self, buffsize, sock):
        """
        Will receive and process data
        param1: int buffsize
        param2: Socket sock
        return: (byte* header, byte* data)
        """
        data, _ = sock.recvfrom(buffsize)
        if len(data) < ct.sizeof(PacketHeader):
            print("Incomplete packet received")
            return None
        
        header = self.parse_packet_header(data)
        return (header, data)
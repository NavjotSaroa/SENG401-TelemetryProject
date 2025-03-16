import fastf1 as ff1
import pandas as pd

ff1.ergast.interface.BASE_URL = "https://api.jolpi.ca/ergast/f1"

class FF1_Interact():
    @staticmethod
    def request_track_list(year):
        """
        Fetches track list from the Fast F1 library

        Args:
            - year: int

        Returns:
            JSON object of tracks, converted from the pandas dataframe that is received from fastf1,
            0 indexed
        """

        if year < 2019 or year > 2024: # Data is only available between 2019 and 2024
            raise ValueError

        try:
            track_list = ff1.get_event_schedule(year, include_testing = False)["EventName"]    # Retrieve dataframe of track list
            track_list_json = track_list.to_json()                  # Convert dataframe to json
            return track_list_json
        except Exception as e:
            raise RuntimeError

    @staticmethod
    def request_drivers(year, event):
        """
        Fetches drivers list from the Fast F1 library

        Args:
            - year: int
            - event: str

        Returns:
            JSON object of drivers, converted from the pandas dataframe that is received from fastf1,
            keys are the driver's numbers (eg: Charles Leclerc is 16)
        """

        if year < 2019 or year > 2024: # Data is only available between 2019 and 2024
            raise ValueError

        try:
            session = ff1.get_session(year, event, 'Q')           # Retrieve session data (Session object)
            session.load()                                          # Load session to get all data
            drivers = session.results['FullName']                   # Extract dataframe of driver names
            drivers_json = drivers.to_json()                        # Convert dataframe to json
            return drivers_json
        except:
            raise RuntimeError
        
    @staticmethod
    def request_telemetry(year, event, driver):
        """
        Fetches driver's telemetry from the Fast F1 library

        Args:
            - year: int
            - event: str
            - driver: str

        Returns:
            Two dataframes:
                - car_data: Telemetry data for car (Speed, Gear, Brake, Throttle, Distance from start line)
                - circuit_info: Information regarding circuit (eg: Corner distance from start line)
        """
        if year < 2019 or year > 2024: # Data is only available between 2019 and 2024
            raise ValueError

        try:
            session = ff1.get_session(year, event, 'Q')                   # Retrieve session data (Session object)
            session.load()                                                  # Load session to get all data
            fastest_lap = session.laps.pick_drivers(driver).pick_fastest()  # Extract telemetry data 
            car_data = fastest_lap.get_car_data().add_distance()            # Add column for distance (for corner markers)
            car_data_relevant = car_data[[                                  # Don't need the rest of the data
                'Speed', 
                'nGear', 
                'Throttle', 
                'Brake', 
                'Distance'
            ]]

            circuit_info = session.get_circuit_info()                       # Extract circuit information (corner distances)

            return (car_data_relevant, circuit_info)
        
        except Exception as e:
            print(e)

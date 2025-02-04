import fastf1 as ff1
import pandas as pd

ff1.ergast.interface.BASE_URL = "https://api.jolpi.ca/ergast/f1"

class FF1_Interact():
    @staticmethod
    def request_track_list(year):
        try:
            return ff1.get_event_schedule(year)["Country"].to_json()
        except:
            return None

    @staticmethod
    def request_drivers(year, country):
        try:
            session = ff1.get_session(year, country, 'Q')
            session.load()
            return session.results['FullName'].to_json()
        except:
            return None
        
    @staticmethod
    def request_telemetry(year, country, driver):
        try:
            session = ff1.get_session(year, country, 'Q')
            session.load()
            fastest_lap = session.laps.pick_drivers(driver).pick_fastest()
            car_data = fastest_lap.get_car_data().add_distance()
            circuit_info = session.get_circuit_info()
            return (car_data[['Speed', 'nGear', 'Throttle', 'Brake', 'Distance']], circuit_info)
        
        except:
            return None


if __name__ == "__main__":
    data = FF1_Interact.request_telemetry(2018, 'Monaco', 44)
    print(list(data[0]['Brake']))
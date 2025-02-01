import fastf1 as ff1

ff1.ergast.interface.BASE_URL = "https://api.jolpi.ca/ergast/f1"

class FF1_Interact():
    @staticmethod
    def request_track_list(year):
        try:
            return ff1.get_event_schedule(year)["Country"]
        except:
            return None

    @staticmethod
    def request_drivers(year, country):
        try:
            session = ff1.get_session(year, country, 'Q')
            session.load()
            return session.results[['DriverNumber', 'FullName']]
        except:
            return None
        
    def request_telemetry(year, country, driver):
        try:
            session = ff1.get_session(year, country, 'Q')
            session.load()
            fastest_lap = session.laps.pick_drivers(driver).pick_fastest()
            car_data = fastest_lap.get_car_data().add_distance()
            circuit_info = session.get_circuit_info()
            return (car_data[['Speed', 'nGear', 'Throttle', 'Brake', 'Distance']], circuit_info.corners['Distance'])
        
        except:
            return None
    

if __name__ == "__main__":
    season2020 = FF1_Interact.request_telemetry(2018, 'Monaco', 44)
    print(season2020)
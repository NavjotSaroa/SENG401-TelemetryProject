import fastf1 as ff1
import pandas as pd
import json 

from ff1_interact import FF1_Interact

ff1.ergast.interface.BASE_URL = "https://api.jolpi.ca/ergast/f1"
ff1.Cache.enable_cache('backend\services\cache')

for i in range(2021, 2025):
    tracklist = FF1_Interact.request_track_list(i)

    # Debugging: Print tracklist to verify it's updating correctly
    print(f"Year: {i}, Tracklist: {tracklist}")  

    if isinstance(tracklist, str):  
        tracklist = json.loads(tracklist) 

    for key, country in tracklist.items():
        drivers = FF1_Interact.request_drivers(i, country)

        if isinstance(drivers, str): 
            drivers = json.loads(drivers) 

        for driver_key, driver in drivers.items():
            try:
                print(f"Fetching telemetry for {i} - {country} - {driver}")
                telemetry = FF1_Interact.request_telemetry(i, country, driver_key)
            except Exception as e:
                print(f"ERROR fetching telemetry for {i} - {country} - {driver}: {e}")
                raise



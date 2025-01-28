import fastf1
import pandas as pd

# Enable FastF1 cache
fastf1.Cache.enable_cache('./cache')

def fetch_telemetry_data(year, track, session_type, driver):
    """
    Fetch telemetry data for a specific driver, track, and session.

    Args:
        year (int): Year of the session.
        track (str): Track name or round number.
        session_type (str): Session type ('FP1', 'FP2', 'FP3', 'Q', 'R').
        driver (str): Driver identifier (eg. 'VER' for Verstappen).

    Returns:
        dict: Processed telemetry data as a dictionary.
    """
    try:
        # Load session data
        session = fastf1.get_session(year, track, session_type)
        session.load()

        # Get telemetry for the specified driver
        driver_data = session.laps.pick_driver(driver).pick_fastest()
        telemetry = driver_data.get_telemetry()  # Contains: time, speed, rpm, gear, throttle, brake, distance

        # Convert telemetry data to dict
        telemetry_dict = telemetry.to_dict(orient='list')

        # Handle serialization of non-standard types (Timedelta and Timestamp are not types supported by jsonify)
        for key, values in telemetry_dict.items():
            telemetry_dict[key] = [
                str(value) if isinstance(value, (pd.Timedelta, pd.Timestamp)) else value
                for value in values
            ]

        return telemetry_dict

    except Exception as e:
        raise RuntimeError(f"Failed to fetch telemetry data: {e}")

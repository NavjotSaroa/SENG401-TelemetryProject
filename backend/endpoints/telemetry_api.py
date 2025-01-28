from flask import Blueprint, request, jsonify
import fastf1
from fastf1 import get_session
import pandas as pd

# Initialize blueprint
telemetry_api = Blueprint("telemetry_api", __name__)

# Enable cache with its dir
fastf1.Cache.enable_cache('./cache')

# Route to fetch telemetry data for a specific driver, track, and session
@telemetry_api.route('/fetch', methods=['GET'])
def fetch_telemetry():
    try:
        # Extract query params
        year = int(request.args.get('year'))
        track = request.args.get('track')   # Track name or round number
        session_type = request.args.get('session')  # 'FP1', 'Q', 'R'
        driver = request.args.get('driver') # Driver identifier (eg.'VER' for Verstappen)

        # Validate input... to be put in models dir?
        if not year or not track or not session_type or not driver:
            return jsonify({"error": "Missing required parameters: year, track, session, driver"}), 400

        # Load session data (using fastf1 func)
        session = get_session(year, track, session_type)
        session.load()

        # Extract telemetry for the specified driver
        driver_data = session.laps.pick_driver(driver).pick_fastest()   # Fastest lap
        telemetry = driver_data.get_telemetry() # Contains: time, speed, rpm, gear, throttle, brake, distance

        # Convert telemetry data to dict 
        telemetry_dict = telemetry.to_dict(orient='list')

        # Handle serialization of non-standard types (Timedelta and Timestamp types were giving problems due to not being supported by jsonify)
        for key, values in telemetry_dict.items():
            telemetry_dict[key] = [
                str(value) if isinstance(value, (pd.Timedelta, pd.Timestamp)) else value
                for value in values
            ]

        # Return telemetry as JSON
        return jsonify({
            "year": year,
            "track": track,
            "session": session_type,
            "driver": driver,
            "telemetry": telemetry_dict
        })
    except Exception as e:
        print(f"Error fetching telemetry: {e}")
        return jsonify({"error": "Failed to fetch telemetry data. Please check your inputs."}), 500

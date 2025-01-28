from flask import Blueprint, request, jsonify
from services.telemetry_service import fetch_telemetry_data

# Initialize blueprint
telemetry_api = Blueprint("telemetry_api", __name__)

@telemetry_api.route('/fetch', methods=['GET'])
def fetch_telemetry():
    """
    API endpoint to fetch telemetry data for a specific driver, track, and session.
    """
    try:
        # Extract query params
        year = request.args.get('year')
        track = request.args.get('track')
        session_type = request.args.get('session')  # 'FP1', 'FP2', 'FP3', 'Q', 'R'
        driver = request.args.get('driver')

        # Validate inputs
        if not year or not track or not session_type or not driver:
            return jsonify({"error": "Missing required parameters: year, track, session, driver"}), 400

        # Convert year to int (had a problem with this earlier)
        try:
            year = int(year)
        except ValueError:
            return jsonify({"error": "Year must be a valid integer."}), 400

        # Fetch telemetry data using the service. Returns as a dict
        telemetry_data = fetch_telemetry_data(year, track, session_type, driver)

        # Return telemetry as JSON
        return jsonify({
            "year": year,
            "track": track,
            "session": session_type,
            "driver": driver,
            "telemetry": telemetry_data
        })

    except RuntimeError as e:
        # Catch errors raised in the service layer
        print(f"Error in service layer: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Catch other errors??
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@telemetry_api.route('/exampleRouteHere', methods=['POST'])
def post_telemetry():
    try:
        ...
    except:
        ...
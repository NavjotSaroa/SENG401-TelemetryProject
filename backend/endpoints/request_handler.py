from flask import Blueprint, request, send_file, abort, jsonify
from services.ff1_interact import FF1_Interact
from middleware.auth import jwt_required
from services.plotter import Plotter
from matplotlib import pyplot as plt
from services.gpt_service import *
import base64
import pandas as pd
import json
import io

# Initialize blueprint
request_handler = Blueprint("telemetry_api", __name__)

@request_handler.route('/fetch/tracklist', methods = ['GET'])
def fetch_tracklist():
    """
    Returns a json of tracks for the queried race weekend.

    Args:
        None, arguments as passed as query with parameter:
            - 'year', between 2019 and 2024

    Returns:
        track_list: JSON object with the tracks for the chosen season. Formatted as follows.    
        {
            "0": "track_0",
            "1": "track_1",
            ...
        }
    """

    try:
        # Extract args from query
        season = int(request.args.get('year'))

        if not season:
            raise ValueError("Season not provided.")

        if season < 2019 or season > 2024:  
            raise ValueError("Invalid season. Year must be between 2019 and 2024.")

        # Request track list from Fast F1 library through FF1_Interact
        track_list = FF1_Interact.request_track_list(season)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return track_list

@request_handler.route('/fetch/drivers', methods = ['GET'])
def fetch_drivers():
    """
    Returns a json of drivers for the queried race weekend.

    Args:
        None, arguments as passed as query with parameters: 
        - 'year', between 2019 and 2024
        - 'track', chosen from track_list from fetch_tracklist

    Returns:
        driver_list: JSON object with the drivers who participated in the chosen race-weekend's 
        qualifying, along with the driver number.
        {
            "driver0_number": "driver0",
            "driver1_number": "driver1",
            ...
        }
    """

    try:
        # Extract args from query
        season = int(request.args.get('year'))
        track = request.args.get('track')   # Fast F1 actually does a fuzzy match and guesses track name, so this will never fail. It will just provided unexpected results if the name is invalid. But it won't break the website.

        if not season:
            raise ValueError("Season not provided.")

        if season < 2019 or season > 2024:  # Data is only available between 2019 and 2024
            raise ValueError("Invalid season. Year must be between 2019 and 2024.")

        # Request driver list from Fast F1 library through FF1_Interact
        driver_list = FF1_Interact.request_drivers(season, track)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return driver_list

def extract_args(args):
    """
        Extracts the args, and retrieves relevant telemetry data and returns them as a tuple.
    """
    season = int(args.get('year'))
    track = args.get('track')
    driver = args.get('driver')
    theme = args.get('theme')
    telemetry = FF1_Interact.request_telemetry(season, track, driver)

    return (season, track, driver, theme, telemetry)

def plot_helper(args, car_data = None):
    """
    Produces png plot of the chosen driver's fastest qualifying lap for the selected race weekend.
    (Displays speed, throttle usage, brake usage, gear usage vs. distance from start line)

    Args:
        None, arguments are passed as query with parameters:
        - 'year', between 2019 and 2024
        - 'track', chosen from track_list from fetch_tracklist
        - 'driver', chosen from fetch_drivers()

    Returns:
        PNG image of the plot
    """
    try:
        # Extract args from query
        _, _, _, theme, telemetry = extract_args(args)

        # Might have to change to .empty
        if car_data is None or car_data.empty:    # This would mean this is a pro driver plot, otherwise, the car_data would be provided by the user
            car_data = telemetry[0]
        
        circuit_info = telemetry[1]

        plot_data = Plotter.plotting(car_data, circuit_info)    # Produces baseline matplotlib plot of telemetry
        Plotter.styling(plot_data, theme)                 # Styles baseline plot

        # Saves and sends PNG of plot
        image_io = io.BytesIO()
        plt.savefig(image_io, format = 'png', bbox_inches = 'tight')
        image_io.seek(0)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        return send_file(image_io, mimetype = 'image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 403



@request_handler.route('/fetch/telemetry', methods = ['GET'])
def fetch_pro_plot():
    """
    Returns a json of drivers for the queried race weekend.

    Args:
        None, arguments as passed as query with parameters: 
        - 'year', between 2019 and 2024
        - 'track', chosen from track_list from fetch_tracklist
        - 'driver', chosen from list of drivers from fetch_drivers
        - 'theme', chosen from dropdown in frontend

    Returns:
        A telemetry plot as a png of the pro_driver data
    """
    return plot_helper(request.args, None)   # Make plot


@request_handler.route('/fetch/registered_telemetry', methods = ['GET'])
@jwt_required
def fetch_user_plot():
    """
    Returns a json of drivers for the queried race weekend.

    Args:
        None, arguments as passed as query with parameters: 
        - 'year', between 2019 and 2024
        - 'track', chosen from track_list from fetch_tracklist
        - 'driver', chosen from list of drivers from fetch_drivers (this is the pro driver)
        - 'theme', chosen from dropdown in frontend
        - 'user_data', JSON of the user's telemetry data (collection is explained on the upload page)

    Returns:
        A telemetry plot as a png of the user's telemetry
    """
    json_file_as_string = request.args.get("user_data")
    json_file = json.loads(json_file_as_string) if json_file_as_string else abort(403)

    user_data = pd.DataFrame.from_dict(json_file)
    user_data = user_data.astype(float)
    user_data.index = user_data.index.astype(int)

    return plot_helper(request.args, user_data)
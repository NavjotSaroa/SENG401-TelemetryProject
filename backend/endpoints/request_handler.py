from flask import Blueprint, request, send_file, abort
from services.ff1_interact import FF1_Interact
from services.plotter import Plotter
from matplotlib import pyplot as plt
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

        if season < 2019 or season > 2024:  
            abort(400)

        # Request track list from Fast F1 library through FF1_Interact
        track_list = FF1_Interact.request_track_list(season)
    except Exception as e:
        abort(404)

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
        track = request.args.get('track')   # Fast F1 actually does a fuzzy matching and guesses track name, so this will never fail

        if season < 2019 or season > 2024:  # Data is only available between 2019 and 2024
            abort(400)

        # Request driver list from Fast F1 library through FF1_Interact
        driver_list = FF1_Interact.request_drivers(season, track)
    except Exception as e:
        abort(400)

    return driver_list

@request_handler.route('/fetch/telemetry', methods = ['GET'])
def fetch_plot():
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
        season = int(request.args.get('year'))
        track = request.args.get('track')
        driver = request.args.get('driver')

        # Request relevant telemetry data from the Fast F1 library through FF1_Interact
        car_data, circuit_info = FF1_Interact.request_telemetry(season, track, driver)

        plot_data = Plotter.plotting(car_data, circuit_info)    # Produces baseline matplotlib plot of telemetry
        Plotter.styling(plot_data, 'cyberpunk')                 # Styles baseline plot
        # TODO: Make this more dynamic for users

        # Saves and sends PNG of plot
        image_io = io.BytesIO()
        plt.savefig(image_io, format = 'png', bbox_inches = 'tight')
        image_io.seek(0)

    except Exception as e:
        abort(400)

    try:
        return send_file(image_io, mimetype = 'image/png')
    except Exception as e:
        abort(403)



from flask import Blueprint, request, send_file
from services.ff1_interact import FF1_Interact
from services.plotter import Plotter
from matplotlib import pyplot as plt
import io

# Initialize blueprint
request_handler = Blueprint("telemetry_api", __name__)

@request_handler.route('/fetch/tracklist', methods = ['GET'])
def fetch_tracklist():
    """
    Returns a json of tracks for the queried year.
    Will show as follows:
    {
        "0": "track_0",
        "1": "track_1",
        ...
    }
    """
    season = request.args.get('year')
    track_list = FF1_Interact.request_track_list(int(season))
    print(track_list)
    return track_list

@request_handler.route('/fetch/drivers', methods = ['GET'])
def fetch_drivers():
    """
    Returns a json of drivers for the queried race weekend.
    Will show as follows:
    {
        "driver0_number": "driver0",
        "driver1_number": "driver1",
        ...
    }
    """
    season = request.args.get('year')
    track = request.args.get('track')
    driver_list = FF1_Interact.request_drivers(int(season), track)
    return driver_list

@request_handler.route('/fetch/telemetry', methods = ['GET'])
def fetch_plot():
    """
    Returns a png of the plotted data for the chosen driver
    """
    season = request.args.get('year')
    track = request.args.get('track')
    driver = request.args.get('driver')

    car_data, circuit_info = FF1_Interact.request_telemetry(int(season), track, driver)
    plot_data = Plotter.plotting(car_data, circuit_info)
    Plotter.styling(plot_data, 'cyberpunk')

    image_io = io.BytesIO()
    plt.savefig(image_io, format = 'png', bbox_inches = 'tight')
    image_io.seek(0)

    return send_file(image_io, mimetype = 'image/png')




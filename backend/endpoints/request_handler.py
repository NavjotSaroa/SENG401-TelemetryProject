from flask import Blueprint, request, send_file, abort
from services.ff1_interact import FF1_Interact
from middleware.auth import jwt_required
from services.plotter import Plotter
from matplotlib import pyplot as plt
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
        season = int(args.get('year'))
        track = args.get('track')
        driver = args.get('driver')
        theme = args.get('theme')
        telemetry = FF1_Interact.request_telemetry(season, track, driver)

        if not car_data:    # This would mean this is a pro driver plot, otherwise, the car_data would be provided by the user
            car_data = telemetry[0]
        
        circuit_info = telemetry[1]

        plot_data = Plotter.plotting(car_data, circuit_info)    # Produces baseline matplotlib plot of telemetry
        Plotter.styling(plot_data, theme)                 # Styles baseline plot

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



@request_handler.route('/fetch/telemetry', methods = ['GET'])
def fetch_pro_plot():
    return plot_helper(request.args, None)   # Make plot


@request_handler.route('/fetch/unregistered_LLM_and_pdf', methods=['GET'])
def fetch_pro_pdf():

    _, _, driver, _, telemetry = extract_args(request.args)
    data = telemetry[0]
    circuit_info = telemetry[1]
    summary_text = single_driver_analysis(driver, data, circuit_info)

    output_pdf = f"{driver}_telemetry_report.pdf"
    pdf_maker = UnregisteredUserPDFMaker(output_pdf)
    pdf_maker.generate_pdf(driver, summary_text)

    return jsonify({
        "driver": driver,
        "summary_text": summary_text,
        "pdf_url": f"/fetch/download_pdf?file={output_pdf}"
    })

@request_handler.route('/fetch/unregistered_download_pdf', methods=['GET'])
def unregistered_download_pdf():
    file_path = request.args.get("file")
    return send_file(file_path, as_attachment=True) if file_path else abort(403)


@request_handler.route('/fetch/registered_telemetry', methods = ['GET'])
@jwt_required
def fetch_user_plot():
    json_file_as_string = request.args.get("user_data")
    json_file = json.loads(json_file_as_string) if json_file_as_string else abort(403)

    user_data = pd.DataFrame.from_dict(json_file)
    user_data = user_data.astype(float)
    user_data.index = user_data.index.astype(int)

    return plot_helper(request.args, user_data)



@request_handler.route('/fetch/registered_LLM_and_pdf', methods=['GET'])
@jwt_required
def fetch_user_pdf():

    _, _, driver, _, telemetry = extract_args(request.args)
    pro_data = telemetry[0]
    circuit_info = telemetry[1]

    json_file_as_string = request.args.get("user_data")
    json_file = json.loads(json_file_as_string) if json_file_as_string else abort(403)

    user_data = pd.DataFrame.from_dict(json_file)
    user_data = user_data.astype(float)
    user_data.index = user_data.index.astype(int)

    summary_text = comparative_analysis(driver, user_data, pro_data, circuit_info)

    output_pdf = f"{driver}_telemetry_report.pdf"
    pdf_maker = RegisteredUserPDFMaker(output_pdf)
    pdf_maker.generate_pdf(driver, summary_text)

    return jsonify({
        "driver": driver,
        "summary_text": summary_text,
        "pdf_url": f"/fetch/download_pdf?file={output_pdf}"
    })

@request_handler.route('/fetch/registered_download_pdf', methods=['GET'])
@jwt_required
def registered_download_pdf():
    file_path = request.args.get("file")
    return send_file(file_path, as_attachment=True) if file_path else abort(403)
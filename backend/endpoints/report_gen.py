from flask import Blueprint, request, jsonify
import pandas as pd
import json
from services.ff1_interact import FF1_Interact
from middleware.auth import jwt_required
from dotenv import load_dotenv
from services.gpt_service import single_driver_analysis, comparative_analysis

# Initialize blueprint
report_gen_api = Blueprint("report_gen_api", __name__)

load_dotenv()

@report_gen_api.route('/single-analysis', methods=['POST'])
@jwt_required
def single_gpt():
    try:
        season, track, driver, _, telemetry = extract_args(request.args)
        data, circuit_info = telemetry

        # Check if the result returned an error
        result = single_driver_analysis(track, data, circuit_info)
        if isinstance(result, Exception):
            return jsonify({"error": str(result)}), 500

        return jsonify({"result": result.content}), 200

    except Exception as e:
        return jsonify({"error": e}), 400




@report_gen_api.route('/comparative-analysis', methods=['POST'])
@jwt_required
def comparative_gpt():
    try:
        _, _, driver, _, telemetry = extract_args(request.args)
        pro_data = telemetry[0]
        circuit_info = telemetry[1]

        setup_data = extract_setup_args(request.args)

        json_file_as_string = request.args.get("user_data")
        json_file = json.loads(json_file_as_string) if json_file_as_string else abort(403)

        user_data = pd.DataFrame.from_dict(json_file)
        user_data = user_data.astype(float)
        user_data.index = user_data.index.astype(int)

        result = comparative_analysis(driver, user_data, pro_data, circuit_info, setup_data)
        if isinstance(result, Exception):
            return jsonify({"error": str(result)}), 500

        return jsonify({"result": result.content}), 200

    except Exception as e:
        return jsonify({"error": e}), 400


def extract_args(args):
    season = int(args.get('year'))
    track = args.get('track')
    driver = args.get('driver')
    theme = args.get('theme')
    telemetry = FF1_Interact.request_telemetry(season, track, driver)

    return (season, track, driver, theme, telemetry)

def extract_setup_args(args):
        setup_data = {
            "frontCamber": args.get("frontCamber"),
            "frontSuspension": args.get("frontSuspension"),
            "frontWingAero": request.args.get("frontWingAero"),
            "onThrottleDiff": args.get("onThrottleDiff"),
            "rearCamber": args.get("rearCamber"),
            "rearSuspension": args.get("rearSuspension"),
            "rearWingAero": args.get("rearWingAero")
        }

        return setup_data
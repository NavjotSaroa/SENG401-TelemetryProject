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
def single_gpt():
    try:
        season, track, driver, _, telemetry = extract_json(request.json)
        data, circuit_info = telemetry

        print("track", track)
        print("data", data)
        print("circuit info", circuit_info)

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
        season, track, driver, _, telemetry = extract_json(request.json)
        setup_data = extract_setup_json(request.json)
        pro_data, circuit_info = telemetry
        user_data = request.json.get("user_data")
        setup_data = request.json.get("setup_data")

        print("track", track)
        print("user data", user_data)
        print("pro data", pro_data)
        print("circuit info", circuit_info)
        print("setup data", setup_data)

        # Check if the result returned an error
        result = comparative_analysis(track, user_data, pro_data, circuit_info, setup_data)
        if isinstance(result, Exception):
            return jsonify({"error": str(result)}), 500

        return jsonify({"result": result.content}), 200

    except Exception as e:
        return jsonify({"error": e}), 400


def extract_json(args):
    season = int(args.get('year'))
    track = args.get('track')
    driver = args.get('driver')
    theme = args.get('theme')
    telemetry = FF1_Interact.request_telemetry(season, track, driver)

    return (season, track, driver, theme, telemetry)

def extract_setup_json(args):
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
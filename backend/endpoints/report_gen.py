from flask import Blueprint, request, jsonify
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
        track = request.args.get("track")
        data = request.args.get("data")

        # Check if the result returned an error
        result = single_driver_analysis(track, data)
        if isinstance(result, Exception):
            return jsonify({"error": str(result)}), 500

        return jsonify({"result": result.content}), 200

    except Exception as e:
        return jsonify({"error": e}), 400




@report_gen_api.route('/comparative-analysis', methods=['POST'])
@jwt_required
def comparative_gpt():
    try:
        track = request.args.get("track")
        user_data = request.args.get("user_data")
        pro_data = request.args.get("pro_data")

        # Check if the result returned an error
        result = comparative_analysis(track, user_data, pro_data)
        if isinstance(result, Exception):
            return jsonify({"error": str(result)}), 500

        return jsonify({"result": result.content}), 200

    except Exception as e:
        return jsonify({"error": e}), 400

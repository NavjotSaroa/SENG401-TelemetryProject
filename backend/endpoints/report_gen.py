from flask import Blueprint, request, jsonify
from middleware.auth import jwt_required
from dotenv import load_dotenv
from services.gpt_service import single_driver_analysis

# Initialize blueprint
report_gen_api = Blueprint("report_gen_api", __name__)

load_dotenv()

@report_gen_api.route('/generate', methods=['POST'])
@jwt_required
def generate():
    try:
        track = request.args.get("track")
        data = request.args.get("data")

        # Check if the result returned an error
        result = single_driver_analysis(track, data)
        if isinstance(result, Exception):
            return jsonify({"error": str(result)}), 500

        return jsonify({"result": result.content}), 200

    except Exception as e:
        return jsonify({"error": e})


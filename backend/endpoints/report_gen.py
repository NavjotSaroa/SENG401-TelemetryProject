from flask import Blueprint, request, jsonify
from middleware.auth import jwt_required
import os
from dotenv import load_dotenv
from openai import OpenAI

# Initialize blueprint
report_gen_api = Blueprint("report_gen_api", __name__)

load_dotenv()

@report_gen_api.route('/generate', methods=['POST'])
@jwt_required
def generate():
    try:
        client = OpenAI(api_key = os.getenv("OPENAI_KEY"))

        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            store = True,
            messages = [
                {"role": "user", "content": "write me a short paragraph explaining how to cook."}
            ]
        )
        # print(completion.choices[0].message)
        message = completion.choices[0].message
        return str(message.content)

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        ...

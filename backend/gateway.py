from flask import Flask, jsonify
from flask_cors import CORS
from endpoints.request_handler import request_handler
from endpoints.data_analysis import data_analysis_api
from endpoints.report_gen import report_gen_api
from endpoints.auth import auth_api
import os

app = Flask(__name__)

CORS(app, origins="http://localhost:3000", supports_credentials=True)

# Registering API endpoints
app.register_blueprint(request_handler, url_prefix='/api/telemetry')
app.register_blueprint(data_analysis_api, url_prefix='/api/data_analysis')
app.register_blueprint(report_gen_api, url_prefix='/api/report_gen')
app.register_blueprint(auth_api, url_prefix='/api/auth')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))   # 10000 is default for render
    app.run(host='0.0.0.0', port = 3001)

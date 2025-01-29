from flask import Flask, jsonify
from endpoints.telemetry_api import telemetry_api
from endpoints.data_analysis import data_analysis_api
from endpoints.report_gen import report_gen_api
from endpoints.auth import auth_api

app = Flask(__name__)

# Registering API endpoints
app.register_blueprint(telemetry_api, url_prefix='/api/telemetry')
app.register_blueprint(data_analysis_api, url_prefix='/api/data_analysis')
app.register_blueprint(report_gen_api, url_prefix='/api/report_gen')
app.register_blueprint(auth_api, url_prefix='/api/auth')

if __name__ == "__main__":
    app.run(host='localhost', port=3000, debug=True)

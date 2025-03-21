import requests
import pytest

BASE_URL = "https://seng401-telemetryproject-d3hw.onrender.com" 

# Fetch tracklist
def test_fetch_tracklist_valid_request():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/tracklist?year=2019")  # use your real API URL
    assert response.status_code == 200

def test_fetch_tracklist_invalid_year_lower():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/tracklist?year=2018")
    assert response.status_code == 400

def test_fetch_tracklist_invalid_year_upper():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/tracklist?year=2025")
    assert response.status_code == 400

def test_fetch_tracklist_invalid_year_not_number():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/tracklist?year=apple")
    assert response.status_code == 400

# Fetch drivers
def test_fetch_drivers_valid_request():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/drivers?year=2019&track=monaco")  # use your real API URL
    assert response.status_code == 200

def test_fetch_drivers_invalid_year_lower():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/drivers?year=2018&track=monaco")
    assert response.status_code == 400

def test_fetch_drivers_invalid_year_upper():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/drivers?year=2025&track=monaco")
    assert response.status_code == 400

def test_fetch_drivers_invalid_year_not_number():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/drivers?year=apple&track=monaco")
    assert response.status_code == 400

# Fetch pro plot
def test_fetch_pro_plot_valid_request_string_driver():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/telemetry?year=2023&track=saudi&driver=HAM")
    assert response.status_code == 200

def test_fetch_pro_plot_valid_request_number_driver():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/telemetry?year=2023&track=saudi&driver=16")
    assert response.status_code == 200

def test_fetch_pro_plot_invalid_request_string_driver():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/telemetry?year=2023&track=saudi&driver=NAV")
    assert response.status_code == 400

def test_fetch_pro_plot_invalid_request_number_driver():
    response = requests.get(f"{BASE_URL}/api/telemetry/fetch/telemetry?year=2023&track=saudi&driver=100")
    assert response.status_code == 400


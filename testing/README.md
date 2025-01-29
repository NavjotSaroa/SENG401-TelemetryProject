# Exploratory Quick Testing
To test, use tools like Postman, or VSCode extension `ThunderClient`.
## 1. Run the Backend
```bash
cd backend/
python gateway.py
``` 
## 2.1 Select and Run the Tests
Open the `backend_test.rest` file and simply click on the "Send Request" button above whichever test you want to run.

## 2.2 Edit the Tests
You can edit the HTTP request sent to the backend simply by editing the URL, method, or parameters. You can make more tests by first typing '###' on a new line, followed by another new line with the next test method and URL.

Example response structure for `telemetry_api.py`:
```json
{
    "year": 2022,
    "track": "Monza",
    "session": "Q",
    "driver": "LEC",
    "telemetry": {
        "Time": ["00:01.000", "00:01.100", "..."],
        "Speed": [220, 221, "..."],
        "Throttle": [100, 100, "..."],
        "Brake": [0, 0, "..."],
        "RPM": [15000, 15100, "..."],
        "Gear": [7, 8, "..."],
        "Distance": [0, 100, "..."]
    }
}
```
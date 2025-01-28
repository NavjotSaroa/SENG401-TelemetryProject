To test, use tools like Postman, or VSCode extension `ThunderClient`. Open the `backend_test.rest` file and simply click on the "Send Request" button.

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
## File structure:
```
backend/
├── middleware/ 
│   ├── db_connection.py      # Handles MySQL DB connection
│   ├── auth.py               # Handles JWT authentication & authorization
│
├── services/
│   ├── telemetry_service.py  # Fetches F1 telemetry data (FastF1)
│   ├── analysis_service.py   # Uses OpenAI's LLM for insights
│   ├── report_service.py     # Generates PDF/image reports
│
├── endpoints/
│   ├── telemetryApi.py       # Handles F1 telemetry API routes
│   ├── dataAnalysis.py       # Handles data analysis API routes
│   ├── reportGen.py          # Handles report generation API routes
│
├── models/
│   ├── telemetry_model.py    # Defines telemetry JSON schema
│   ├── user_model.py         # Defines user authentication schema
│
├── utils/
│   ├── helper.py             # Common utility/helper functions?
│
├── config.py                 # Stores environment variables (secrets, DB config)
├── gateway.py                # API Gateway (single entry point)
├── requirements.txt          # Python dependencies?
├── vercel.json               # Vercel configuration file
└── README.md                 # Documentation
```

## System Flow:
1. Frontend requests data - react app sends API request to backend
2. API gateway handles request - redirects request to appropriate endpoint
3. Middleware authenticates user - JWT validation for registered users / protected routes
4. DB connection middleware (if needed) - fetches user data and loads it in-mem
5. Service request - call the required service
6. Send response to frontend - return data for visualization

## Architecture Details
The backend is structured in a **layered architecture** consisting of:
1. Presentation Layer - `endpoints/telemetry_api.py`, `endpoints/data_analysis.py`, `endpoints/report_gen.py`. These are RESTful API endpoints that handle incoming HTTP requests from the frontend. They pass data to the service layer, as well as return structured responses to the client (frontend).
2. Business Logic / Service Layer - `services/telemetry_service.py`, `services/data_analysis.py`, `services/report_service.py`. The service layer contains the core logic for processing and analyzing the telemetry data. It interacts with external libraries to fetch telemetry data, and to utilize OpenAI's API.
3. Data Access Layer - `middleware/db_connection.py`. Handles database interactions. 
4. Middleware Layer - `middleware/auth.py`. Handles user authentication using JWT's.

This layered structure makes it so that the backend has a clear separation of concerns, where each layer has a different responsibility. This also makes the backend more modular, and thus we can easily modify one layer without affecting the others. Lastly, each layer can be tested seperately, making unit testing easier. 
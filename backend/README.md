## File structure:
```
backend/
├── middleware/ 
│   ├── db_connection.py      # Handles MySQL DB connection
│   ├── auth.py               # Handles JWT generation, authentication & authorization
│
├── services/
│   ├── telemetry_service.py  # Fetches F1 telemetry data (FastF1)
│   ├── analysis_service.py   # Uses OpenAI's LLM for insights
│   ├── report_service.py     # Generates PDF/image reports
│   ├── delete_account.py     # Deletes user from DB
│   ├── ff1_interact.py       # Provides several services interacting with fastf1
│   ├── login.py              # Checks credentials on DB, then generates and returns a JWT token
│   ├── plotter.py            # Creates a plot given certain parameters. 
│   ├── register.py           # Saves a user and hashed password in DB
│   ├── styling.py            # Styles the plots according to style chosen by the user
│
├── endpoints/
│   ├── telemetryApi.py       # Handles F1 telemetry API routes
│   ├── dataAnalysis.py       # Handles data analysis API routes
│   ├── reportGen.py          # Handles report generation API routes??
│   ├── auth.py               # Handles user authentication API routes
│
├── gateway.py                # API Gateway (single entry point)
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel configuration file
├── styles.json               # Plot styles costumization presets
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

## API Rate Limits
- fastf1: When rate limits are exceeded, FastF1 will either…
  - throttle the rate of requests, if small delays are sufficient to stay within the limit (soft rate limit)
  - raise a `fastf1.RateLimitExceededError` (hard rate limit)
- OpenAI: 

## Generative AI Disclosure:
ChatGPT was used in debugging and identification of errors in the code, along with assistance in deployment.
Beyond that, it was also used from an educational perspective to understand unfamiliar technologies before code was written in ourselves.
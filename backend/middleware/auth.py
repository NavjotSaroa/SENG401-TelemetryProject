from flask import request, jsonify
from functools import wraps
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Secret for JWT en/decoding
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
token_exp_hours = 1

def generate_jwt(user_id, username):
    """
    Generate a JWT token for authenticated users.
    """
    try:
        expiration_time = datetime.now() + timedelta(hours=token_exp_hours)
        
        payload = {
            "user_id": user_id,
            "username": username,
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return None
        
def verify_jwt(token):
    """
    Verify the JWT token and return user data if valid.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired. Please log in again."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token. Please log in again."}
        
def jwt_required(f):
    """
    Decorator to enforce JWT authentication on protected routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # Get the token from the request headers
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Authorization token is missing."}), 401
        
        decoded_token = verify_jwt(token)
        
        if "error" in decoded_token:
            return jsonify(decoded_token), 401

        # Attach user data to request
        request.user = decoded_token
        return f(*args, **kwargs)

    return decorated_function 
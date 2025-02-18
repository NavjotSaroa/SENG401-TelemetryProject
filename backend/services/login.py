import bcrypt
from middleware.db_connection import get_db_connection
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def login_user(username, password):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username))
            user = cursor.fetchone()
            
            if not user:
                raise ValueError("Invalid username or password")
            
            user_id, stored_password_hash = user["id"], user["password_hash"]
            
            if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                raise ValueError("Incorrect password for the given user")
            
            # Generate JWT token... everything above works without jwt stuff
            token = jwt.encode(
                {
                    "user_id": user_id,
                    "username": username,
                },
                SECRET_KEY,
                algorithm="HS256"
            )
            print(token)    # DEBUGGING ONLY
            return token
            
    finally:
        connection.close()
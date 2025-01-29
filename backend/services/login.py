import bcrypt
from middleware.db_connection import get_db_connection

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
            
            # JWT?? Might be a little too much for mvp?
            
    finally:
        connection.close()
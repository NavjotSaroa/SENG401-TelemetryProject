import bcrypt
from middleware.db_connection import get_db_connection

def delete_user_account(username, password):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username))
            user = cursor.fetchone()
            
            # Check if user exists
            if not user:
                raise ValueError("Invalid username or password")
            
            user_id, stored_password_hash = user["id"], user["password_hash"]
            
            # Check passwords
            if not bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                raise ValueError("Incorrect password for the given user")
            
            # Delete user
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id))
            connection.commit()
            
            cursor.execute("DELETE FROM telemetry_data WHERE user_id = %s", (user_id))
            connection.commit()
    finally:
        connection.close()
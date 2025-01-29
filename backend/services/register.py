import bcrypt
from middleware.db_connection import get_db_connection

def register_user(username, password):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Check if username already exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username))
            if cursor.fetchone():
                raise ValueError("Username already exists")
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
            connection.commit()
            
    finally:
        connection.close()
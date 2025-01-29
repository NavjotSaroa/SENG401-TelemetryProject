import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Make and returns a connection to MySQL DB using secrets from .env
    """
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor  # Ensures results are dict. Was giving issues
    )
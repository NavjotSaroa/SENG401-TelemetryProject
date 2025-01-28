import jwt
from functools import wraps

SECRET_KEY = "a_secret_key_goes_here...maybe_in_.env?"

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.InvalidTokenError:
        return None

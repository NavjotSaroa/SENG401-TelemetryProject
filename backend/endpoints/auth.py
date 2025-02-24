from flask import Blueprint, request, jsonify
from services.register import register_user
from services.login import login_user
from services.delete_account import delete_user_account
from middleware.auth import jwt_required

auth_api = Blueprint("auth_api", __name__)

@auth_api.route('/register', methods=['POST'])
def register():
    """
    API endpoint for user registration.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        register_user(username, password)
        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@auth_api.route('/login', methods=['POST'])
def login():
    """
    API endpoint for user login.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    try:
        token = login_user(username, password)
        return jsonify({"message": "User logged in successfully", "token": token, "username": username}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
@auth_api.route('/delete_account', methods=['DELETE'])
@jwt_required
def delete_account():
    """
    API endpoint for deleting user data from the DB.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    try:
        delete_user_account(username, password)
        return jsonify({'message': "Successfully deleted account"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401
        
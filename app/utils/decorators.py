from functools import wraps
from flask import request, jsonify
from app.services.auth_service import AuthService

auth_service = AuthService()

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get credentials from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request data"}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Missing credentials"}), 400
        
        # Authenticate user
        is_valid, message = auth_service.authenticate(username, password)
        if not is_valid:
            return jsonify({"error": "user info error"}), 401
        
        return f(*args, **kwargs)
    return decorated_function 
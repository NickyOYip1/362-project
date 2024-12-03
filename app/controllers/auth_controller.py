from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.decorators import require_auth

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/auth', methods=['POST'])
def authenticate():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Check if credentials are provided
        if not username or not password:
            return jsonify({"error": "Missing credentials"}), 401
        
        # Create user object
        user = User(username, password)
        
        # Validate username format
        if not user.validate_username():
            return jsonify({"error": "Invalid username format"}), 401
            
        # Validate password format
        if not user.validate_password():
            return jsonify({"error": "Invalid password format"}), 401
            
        return jsonify({
            "message": "Authentication successful",
            "status": "OK"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
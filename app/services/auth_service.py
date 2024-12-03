from app.models.user import User

class AuthService:
    def __init__(self):
        self._active_sessions = {}  # In a real app, use proper session management

    def authenticate(self, username: str, password: str) -> tuple[bool, str]:
        """Authenticate a user with username and password"""
        user = User(username, password)
        is_valid, message = user.validate()
        
        if is_valid:
            self._active_sessions[username] = True  # Simple session tracking
            return True, "Authentication successful"
        
        return False, message

    def is_authenticated(self, username: str) -> bool:
        """Check if a user is currently authenticated"""
        return self._active_sessions.get(username, False)

    def logout(self, username: str) -> None:
        """Remove user from active sessions"""
        if username in self._active_sessions:
            del self._active_sessions[username] 
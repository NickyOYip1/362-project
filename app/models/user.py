class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def validate_username(self) -> bool:
        """Validate that username is exactly 4 digits"""
        return len(self.username) == 4 and self.username.isdigit()

    def validate_password(self) -> bool:
        """Validate password format (username + '-pw')"""
        expected_password = f"{self.username}-pw"
        return self.password == expected_password

    def validate(self) -> tuple[bool, str]:
        """Validate both username and password"""
        if not self.validate_username():
            return False, "Invalid username format. Must be exactly 4 digits."
        if not self.validate_password():
            return False, "Invalid password format. Must be 'username-pw'."
        return True, "Valid credentials" 
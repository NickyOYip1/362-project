class Config:
    # Flask settings
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'dev-key-change-in-production'
    
    # Server settings
    HOST = 'localhost'
    PORT = 5000
    
    # Legacy server settings
    LEGACY_HOST = 'localhost'
    LEGACY_TCP_PORT = 31416
    LEGACY_UDP_PORT = 31416
    
    # Redis settings (if using message queue)
    REDIS_URL = 'redis://localhost:6379'

class TestConfig(Config):
    """Test configuration."""
    TESTING = True

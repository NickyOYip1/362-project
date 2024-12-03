from flask import Flask
from config import Config
from app.controllers.pi_controller import pi_blueprint
from app.controllers.legacy_controller import legacy_blueprint
from app.controllers.statistics_controller import statistics_blueprint
from app.controllers.task_controller import task_blueprint
from app.controllers.auth_controller import auth_blueprint

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(pi_blueprint)
    app.register_blueprint(legacy_blueprint)
    app.register_blueprint(statistics_blueprint)
    app.register_blueprint(task_blueprint)
    
    return app
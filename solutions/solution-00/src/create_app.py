""" Initialize the Flask app. """
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.config import Config
from src.config import get_config
from dotenv import load_dotenv

cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class="src.config.DevelopmentConfig") -> Flask:
    """
    Create a Flask app with the given configuration class.
    The default configuration class is DevelopmentConfig.
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.config.from_object(config_class)
    app.config.from_object(get_config())
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)

    db = SQLAlchemy(app)

    return app

from src.__init__ import create_app, db
import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.config import get_config
from dotenv import load_dotenv

# Créez et configurez l'application Flask
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
    cors.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register extensions, routes, handlers if any
    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    return app

# Vérifiez si la base de données SQLite existe, sinon créez-la
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
    database_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if not os.path.exists(database_path):
        with app.app_context():
            db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.config import get_config
from dotenv import load_dotenv
from src.routes import main

# Charger le fichier .env approprié
if os.getenv('FLASK_ENV') == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

# Déclaration des extensions
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
    cors.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register extensions, routes, handlers if any
    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    @app.route('/')
    def home():
        return 'Hello, World!'
    return app

def register_extensions(app):
    pass  # Ajoutez ici l'enregistrement des extensions

def register_routes(app):
    pass  # Ajoutez ici l'enregistrement des routes

def register_handlers(app):
    pass  # Ajoutez ici l'enregistrement des gestionnaires d'erreurs

if __name__ == "__main__":
    app = create_app()

    # Vérifiez si la base de données SQLite existe, sinon créez-la
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        database_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(database_path):
            with app.app_context():
                db.create_all()

    app.run(port=5006)


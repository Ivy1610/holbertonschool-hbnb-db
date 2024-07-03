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

cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
    db = SQLAlchemy(app)

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
    # enregistrement des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

def register_routes(app):
    # enregistrement des routes
    from src.routes import main_routes
    app.register_blueprint(main_routes)

def register_handlers(app):
    # enregistrement des gestionnaires d'erreurs
    @app.errorhandler(404)
    def not_found_error(error):
        return "Page not found", 404

    @app.errorhandler(500)
    def internal_error(error):
        return "Internal server error", 500

if __name__ == '__main__':
    app = create_app()

# Vérifiez si la base de données SQLite existe, sinon créez-la
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        database_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(database_path):
            with app.app_context():
                db.create_all()

app.run(debug=True, port=5006)

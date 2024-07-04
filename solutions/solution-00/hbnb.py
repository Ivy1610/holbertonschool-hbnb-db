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
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    pass

def register_routes(app):
    from src.routes.auth import auth_bp
    from src.routes.protected import protected_bp
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp
    pass 

def register_handlers(app):
    app.errorhandler(404)(lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    )
    )
    app.errorhandler(400)(
        lambda e: (
            {"error": "Bad request", "message": str(e)}, 400
        )
    )
    pass

if __name__ == '__main__':
    app = create_app()

# Vérifiez si la base de données SQLite existe, sinon créez-la
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        database_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(database_path):
            with app.app_context():
                db.create_all()

app.run(debug=True, port=5006)

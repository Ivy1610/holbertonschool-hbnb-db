import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.config import get_config
from dotenv import load_dotenv

load_dotenv()

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

    config_class = get_config()
    app.config.from_object(config_class)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///development.db')
    app.config['USE_DATABASE'] = os.getenv('USE_DATABASE', False)
    db = SQLAlchemy(app)

    
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins: "*""}})
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Register extensions, routes, handlers if any

    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    return app


def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    pass
    # Further extensions can be added here


def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""

    # Import the routes here to avoid circular imports
    from src.routes.auth import auth_bp
    from src.routes.protected import protected_bp
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp

    # Register the blueprints in the app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(protected_bp, url_prefix='/api')
    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)


def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    app.errorhandler(404)(lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    )
    )
    app.errorhandler(400)(
        lambda e: (
            {"error": "Bad request", "message": str(e)}, 400
        )
    )

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
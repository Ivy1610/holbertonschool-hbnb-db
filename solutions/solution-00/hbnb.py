""" Another way to run the app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_classs=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from src.models import user
        db.create_all(app)

    from src.routes import register_routes
    register_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
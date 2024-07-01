"""
User related functionality
"""

from src.models.base import Base, db
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(Base):
    """User representation"""
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(String(120), unique=True, nullable=False)
    first_name = db.Column(String(50), nullable=False)
    last_name = db.Column(String(50), nullable=False)
    password_hash = db.Column(String(128), nullable=False)
    is_admin = db.Column(Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    

    def __init__(self, email: str, first_name: str, last_name: str, password: str, **kwargs):
        """Dummy init"""
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = generate_password_hash(password)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    def set_password(self, password: str) -> bool:
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify the password"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    @staticmethod
    def create(user_data: dict) -> "User":
        """Create a new user"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        if User.query.filter_by(email=user_data["email"]).filter():
            raise ValueError("User already exists")

        new_user = User(**user_data)
        repo.save(new_user)
        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository


        user = User.query.get(user_id)
        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "password" in data:
            user.password_hash = bcrypt.generate_password_hash(data["password"])

        repo.update(user)
        return user

from src.models.place import Place
Place.host = db.relationship("User",  back_populates="places")
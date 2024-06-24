"""
User related functionality
"""

from src.models.base import Base, db
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    """User representation"""
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, email: str, first_name: str, last_name: str, password: str, **kw):
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

    def verify_password(self, password: str) -> bool:
        """Verify the password"""
        return check_password_hash(self.password_hash, password)
    
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
            user.password_hash = generate_password_hash(data["password"])

        repo.update(user)
        return user
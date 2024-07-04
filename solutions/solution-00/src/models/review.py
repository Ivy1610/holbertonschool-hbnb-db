"""
Review related functionality
"""

from src.models.base import BaseModel, db
from src.models.place import Place
from src.models.user import User
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Review(BaseModel):
    """Review representation"""
    __tablename__ = 'reviews'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id = Column(UUID(as_uuid=True), ForeignKey('places.id'), nullable=False) 
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    comment = Column(String(256), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(
        self, place_id: str, user_id: str, comment: str, rating: float, **kwargs) -> None:
        """Dummy init"""
        super().__init__(**kwargs)
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
        self.rating = rating

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Review {self.id} - '{self.comment[:25]}...'>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Review":
        """Create a new review"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        user = User.get(data["user_id"])
        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        place = Place.get(data["place_id"])
        if not place:
            raise ValueError(f"Place with ID {data['place_id']} not found")

        new_review = Review(**data)
        repo.save(new_review)
        return new_review

    @staticmethod
    def update(review_id: str, data: dict) -> "Review | None":
        """Update an existing review"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        review = Review.get(review_id)
        if not review:
            raise ValueError("Review not found")

        for key, value in data.items():
            setattr(review, key, value)

        repo.update(review)
        return review

Review.place = db.relationship('Place', backref=db.backref('reviews', lasy=True))
Review.user = db.relationship('User', backref=db.backref('reviews', lasy=True))
"""
Place related functionality
"""

from src.models.base import BaseModel, db
from src.models.city import City
from src.models.user import User
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid


class Place(BaseModel):
    """Place representation"""
    __tablename__ = 'places'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(String(50), nullable=False)
    description = db.Column(String(256), nullable=False)
    address = db.Column(String(126), nullable=False)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)
    host_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    city_id = db.Column(UUID(as_uuid=True), ForeignKey('cities.id'), nullable=False)
    price_per_night = db.Column(Integer, nullable=False)
    number_of_rooms = db.Column(Integer, nullable=False)
    number_of_bathrooms = db.Column(Integer, nullable=False)
    max_guests = db.Column(Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __init__(self, **kwargs):
        """Dummy init"""
        super().__init__(**kwargs)
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.address = kwargs.get("address", "")
        self.city_id = kwargs["city_id"]
        self.latitude = float(kwargs.get("latitude", 0.0))
        self.longitude = float(kwargs.get("longitude", 0.0))
        self.host_id = kwargs["host_id"]
        self.price_per_night = int(kwargs.get("price_per_night", 0))
        self.number_of_rooms = int(kwargs.get("number_of_rooms", 0))
        self.number_of_bathrooms = int(kwargs.get("number_of_bathrooms", 0))
        self.max_guests = int(kwargs.get("max_guests", 0))

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Place":
        """Create a new place"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()


        user = User.get(data["host_id"])
        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city = City.get(data["city_id"])
        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(**data)
        repo.save(new_place)

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """Update an existing place"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        place = Place.get(place_id)
        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        repo.update(place)

        return place

User.places = relationship("Place", order_by=Place.id, back_populates="host")
City.places = relationship("Place", order_by=Place.id, back_populates="city")
Place.host = relationship("User", back_populates="places")
Place.city = relationship("City", back_populates="places")
"""
Amenity related functionality
"""

from src.models.base import BaseModel, db
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.place import Place
import uuid


class Amenity(BaseModel):
    """Amenity representation"""
    __tablename__ = 'amenities'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(String, nullable=False, unique=True)

    def __init__(self, name: str, **kwargs) -> None:
        """Dummy init"""
        super().__init__(**kwargs)
        self.name = name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        """Create a new amenity"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        amenity = Amenity(**data)
        repo.save(amenity)

        return amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        """Update an existing amenity"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        amenity = Amenity.get(amenity_id)
        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        repo.update(amenity)
        return amenity


class PlaceAmenity(BaseModel):
    """PlaceAmenity representation"""

    __tablename__ = 'place_amenities'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id = Column(UUID(as_uuid=True), ForeignKey('places.id'), nullable=False)
    amenity_id = Column(UUID(as_uuid=True), ForeignKey('amenities.id'), nullable=False)

    def __init__(self, place_id: str, amenity_id: str, **kwargs) -> None:
        """Dummy init"""
        super().__init__(**kwargs)
        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<PlaceAmenity ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":
        """Get a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        place_amenities: list[PlaceAmenity] = repo.get_all("placeamenity")
        for place_amenity in place_amenities:
            if (
                place_amenity.place_id == place_id
                and place_amenity.amenity_id == amenity_id
            ):
                return place_amenity

        return None

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        """Create a new PlaceAmenity object"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        new_place_amenity = PlaceAmenity(**data)
        repo.save(new_place_amenity)

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:
        """Delete a PlaceAmenity object by place_id and amenity_id"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        place_amenity = PlaceAmenity.get(place_id, amenity_id)
        if not place_amenity:
            return False

        repo.delete(place_amenity)
        return True

    @staticmethod
    def update(entity_id: str, data: dict):
        """Not implemented, isn't needed"""
        raise NotImplementedError(
            "This method is defined only because of the Base class"
        )
    
Amenity.plce_amenities = relationship("PlaceAmenity", back_populates="amenity")
    
PlaceAmenity.amenity = relationship("Amenity", back_populates="place_amenities")
PlaceAmenity.place = relationship("Place", back_populates="place_amenities")

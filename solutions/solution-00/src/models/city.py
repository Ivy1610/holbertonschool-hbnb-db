"""
City related functionality
"""

from src.models.base import Base, db
from src.models.country import Country
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
import uuid


class City(Base):
    """City representation"""

    __tablename__ = 'cities'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4))
    name = Column(String(50), nullable=False)
    country_id = Column(String(36), ForeignKey('countries.id'), nullable=False)
    
    
    def __init__(self, name: str, country_id: str, **kwargs) -> None:
        """Dummy init"""
        super().__init__(**kwargs)
        self.name = name
        self.country_id = country_id
    

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": str(self.id),
            "name": self.name,
            "country_id": self.country_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        country = Country.get(data["country_id"])
        if not country:
            raise ValueError("Country not found")

        city = City(**data)
        repo.save(city)

        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        city = City.get(city_id)
        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        repo.update(city)

        return city

Country.cities = relationship("city", order_by=City.id, back_populates="country")
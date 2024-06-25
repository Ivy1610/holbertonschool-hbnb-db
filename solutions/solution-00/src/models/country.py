"""
Country related functionality
"""


from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.models.base import Base, db
import uuid


class Country:
    """
    Country representation

    This class does NOT inherit from Base, you can't delete or update a country

    This class is used to get and list countries
    """
    __tablename__ = 'countries'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4))
    name = Column(String(50), nullable=False)
    code =  Column(String(3), unique=True, nullable=False)
    cities = relationship("city", back_populates="country", cascade="all, delete-orphan")

    def __init__(self, name: str, code: str, **kwargs) -> None:
        """Dummy init"""
        super().__init__(**kwargs)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "id": str(self.id),
            "name": self.name,
            "code": self.code,
            "cities": [city.to_dict() for city in self.cities]
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        return repo.get_all("country")

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        for country in Country.get_all():
            if country.code == code:
                return country
        return None

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()

        country = Country(name=name, code=code)
        repo.save(country)

        return country

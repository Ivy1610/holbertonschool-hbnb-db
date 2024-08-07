""" Abstract base class for all models """
from flash import Flask
from datetime import datetime
from typing import Any, Optional
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from abc import ABC, ABCMeta, abstractmethod
from flask_sqlalchemy import SQLAlchemy
 

db =  SQLAlchemy()


class CustomMeta(ABCMeta, type(db.Model)):
    pass

Base = declarative_base(metaclass=CustomMeta)

class BaseModel(Base):
    """
    Base Interface for all models using SQLAlchemy
    """
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    
    def __init__(self, **kwargs) -> None:
        """
        Base class constructor
        If kwargs are provided, set them as attributes
        """
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                continue
            setattr(self, key, value)

    @classmethod
    def get(cls, id) -> Optional["BaseModel"]:
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()
        return repo.get(cls.__name__.lower(), id)

    @classmethod
    def get_all(cls) -> list["BaseModel"]:
        """
        This is a common method to get all objects of a class

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()
        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, id) -> bool:
        """
        This is a common method to delete an specific
        object of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence.sqlalchemy_repository import SQLAlchemyRepository
        repo = SQLAlchemyRepository()
        obj = cls.get(id)

        if not obj:
            return False

        return repo.delete(obj)

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""
        pass

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""
        pass

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Any:
        """Updates an object of the class"""
        pass

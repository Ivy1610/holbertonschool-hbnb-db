"""SQLAlchemy implementation of the repository patern"""

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from src.models.base import db

DATABASE_URL = 'sqlite:///development.db'

engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

@contextmanager
def session_scope():
    session =Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

class SQLAlchemyRepository:
    """SQLAlchemy repository implentation"""

    def reload(self) -> None:
        db.create_all()
    
    def get_all(self, model_name: str) -> list:
        with session_scope() as session:
            model = db.Model._decl_class_registry.get(model_name)
            return session.query(model).all() if model else []
        
    def get(self, model_name: str, id: str):
        with session_scope() as session:
            model = db.Model._decl_class_registry.get(model_name)
            return session.query(model).get(id) if model else None
        
    def save(self, obj) -> None:
        with session_scope() as session:
            session.add(obj)

    def update(self, obj) -> None:
        with session_scope() as session:
            session.merge(obj)

    def delete(self, obj) -> None:
        with session_scope() as session:
            session.delete(obj)
            return True
""" Populate the database with some data at the start of the application"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

from src.persistence.sqlalchemy_repository import SQLAlchemyRepository


def populate_db(repo: SQLAlchemyRepository) -> None:
    """Populates the db with a dummy country"""
    from src.models.country import Country

    countries = [
        Country(name="Uruguay", code="UY"),
    ]

    for country in countries:
        repo.save(country)

    print("Memory DB populated")

if __name__ == "__main__":

    repo = SQLAlchemyRepository()

    populate_db(repo)

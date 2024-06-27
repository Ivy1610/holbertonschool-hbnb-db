# create_tables.py
from app import db
from models import User
from models import Amenity
from models import City
from models import Country
from models import Place
from models import Review
from models import Base

def create_all_tables():
    db.create_all()

if __name__ == "__main__":
    create_all_tables()


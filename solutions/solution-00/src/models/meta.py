from sqlalchemy.ext.declarative import declarative_base
from abc import ABCMeta

Base = declarative_base()

class CustomMeta(type(Base), ABCMeta):
    pass

Base = declarative_base(metaclass=CustomMeta)

from sqlalchemy.ext.declarative import declarative_base
from abc import ABCMeta



class CustomMeta(type(db.Model), ABCMeta):
    pass

BaseMeta = declarative_base(metaclass=CustomMeta)
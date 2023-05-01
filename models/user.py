#!/usr/bin/python3
from sqlalchemy import Column, MetaData, String
from sqlalchemy.ext.declarative import declarative_base

from models.base_model import BaseModel

"""User model module"""


mymetadata = MetaData()
Base = declarative_base(metadata=mymetadata)


class User(BaseModel):
    """user class definition
    Represent a user model object
    """
    __tablename__ = "users"
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)

    def mapInput(self, *args):
        """ Maps non keyworded arguments

        Parameters:
            [email, password, first_name, last_name]
        """
        [email, password, first_name, last_name] = args
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

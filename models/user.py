#!/usr/bin/python3
from models.base_model import BaseModel
from sqlalchemy import (Column, String, MetaData, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
"""User model module"""


mymetadata = MetaData()
Base = declarative_base(metadata=mymetadata)


class User(BaseModel):
    """user class definition
    Represent a user model object
    """
    __tablename__ = "users"
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

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

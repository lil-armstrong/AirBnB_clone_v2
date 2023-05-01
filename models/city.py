#!/usr/bin/python3
from typing import Tuple, Union

from sqlalchemy import Column, ForeignKey, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

from models.base_model import BaseModel
from models.state import State

"""City model module"""


class City(BaseModel):
    """City class definition
    Represent a City model object
    """
    VALID_ATTR = {'name': str, 'state_id': str}

    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    state = relationship('State',
                         backref=backref('cities',
                                         cascade='all, delete, delete-orphan'))

    def mapInput(self, args: Tuple[str, str]):
        """ Maps non keyworded arguments

        Parameters:
            args (Tuple[name:`str`,state_id:`str`]):\
                Tuple argument
        """
        [name, state_id] = args
        self.name = name
        self.state_id = state_id

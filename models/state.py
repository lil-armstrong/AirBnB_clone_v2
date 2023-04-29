#!/usr/bin/python3
from models.base_model import BaseModel
from typing import Tuple, Union
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, MetaData, ForeignKey)

"""State model module"""


class State(BaseModel):
    """State class definition
    Represent a state model object
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    def mapInput(self, *args: str):
        """ Maps non keyworded arguments

        Parameters:
            args (Tuple[name:`str`]):\
                State attributes arguments

        Returns:
            None
        """
        if len(args) > 0:
            [name] = args
            self.name = name

    @property
    def cities(self):
        """Return a list of City instances with state_id equals to the\
            current State.id"""
        from models import storage
        city_objs = storage.all('City').values()
        return [city_obj
                for city_obj in city_objs
                if city_obj.state_id == self.id]

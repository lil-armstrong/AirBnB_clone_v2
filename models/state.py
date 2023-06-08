#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    def mapInput(self, *args: str):
        """ Maps non keyworded arguments

        Parameters:
            args (Tuple[name:`str`]):\
                State attributes arguments

        Returns:
            None
        """
        if len(args) > 0:
            if type(args[0]) is self.VALID_ATTR['name']:
                self.name = args[0]

    @property
    def cities(self):
        """Return a list of City instances with state_id equals to the\
            current State.id"""
        from models import storage
        city_objs = storage.all('City').values()
        return [city_obj
                for city_obj in city_objs
                if city_obj.state_id == self.id]

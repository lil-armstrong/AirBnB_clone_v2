#!/usr/bin/python3
from sqlalchemy import Column, ForeignKey, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel

"""State model module"""


class State(BaseModel, Base):
    """State class definition
    Represent a state model object
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    # cities = relationship("City", cascade='all, delete, delete-orphan',
    #                       backref="state")

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

#!/usr/bin/python3
from sqlalchemy import Column, String

from models.base_model import BaseModel

"""State model module"""


class State(BaseModel):
    """State class definition
    Represent a state model object
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    VALID_ATTR = {'name': str}

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

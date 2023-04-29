#!/usr/bin/python3
from models.base_model import BaseModel, Base
from typing import Tuple
"""Amenity model module"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Amenity(BaseModel):
    """Amenity class definition
    Represent a Amenity model object
    """
    name: str = ''

    def mapInput(self, *args: str):
        """ Maps non keyworded arguments

        Parameters:
            *args (Tuple[name:`str`]):\
                Amenity attribute argument
        """
        [name] = args
        self.name = name

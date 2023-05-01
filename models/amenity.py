#!/usr/bin/python3
from models.base_model import BaseModel, Base
from typing import Tuple
"""Amenity model module"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class Amenity(BaseModel):
    """Amenity class definition
    Represent a Amenity model object
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    VALID_ATTR = {'name': str}

    def mapInput(self, *args: str):
        """ Maps non keyworded arguments

        Parameters:
            *args (Tuple[name:`str`]):\
                Amenity attribute argument
        """
        [name] = args
        self.name = name

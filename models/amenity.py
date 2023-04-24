#!/usr/bin/python3
from models.base_model import BaseModel
"""Amenity model module"""


class Amenity(BaseModel):
    """Amenity class definition
    Represent a Amenity model object
    """
    name:str = ""

    def __init__(self, *args, **kwargs):
        """Instantiate Amenity object"""
        super().__init__(*args, **kwargs)
    
    def mapInput(self, *args):
        """ Maps non keyworded arguments 
        
        Parameters:
            [name]
        """
        [name] = args
        self.name=name
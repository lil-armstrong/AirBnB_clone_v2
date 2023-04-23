#!/usr/bin/python3
from models.base_model import BaseModel
"""City model module"""


class City(BaseModel):
    """City class definition
    Represent a City model object
    """
    name = ""
    state_id = ""

    def __init__(self, *args, **kwargs):
        """Instantiate City object"""
        super().__init__(*args, **kwargs)

    def mapInput(self, *args):
        """ Maps non keyworded arguments 
        
        Parameters:
            [name, state_id]
        """
        self.name=args[0]
        self.state_id=args[0]
#!/usr/bin/python3
from models.base_model import BaseModel
"""State model module"""


class State(BaseModel):
    """State class definition
    Represent a state model object
    """
    name:str = ""
        
    def mapInput(self, *args):
        """ Maps non keyworded arguments 
        
        Parameters:
            [name]
        """
        
        [name] = args;
        self.name=name
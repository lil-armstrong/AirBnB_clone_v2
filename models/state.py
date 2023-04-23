#!/usr/bin/python3
from models.base_model import BaseModel
"""State model module"""


class State(BaseModel):
    """State class definition
    Represent a state model object
    """
    name = ""
        
    def mapInput(self, *args):
        """ Maps non keyworded arguments 
        
        Parameters:
            [name]
        """
        print(self.__class__.__name__, args[0])
        if(len(args[0]) <=0):
            raise ValueError("[State] Missing name value")
            return
        self.name=args[0]
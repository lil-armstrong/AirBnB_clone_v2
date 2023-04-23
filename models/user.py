#!/usr/bin/python3
from models.base_model import BaseModel
"""User model module"""


class User(BaseModel):
    """user class definition
    Represent a user model object
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """Instantiate User object"""
        super().__init__(*args, **kwargs)
        
    def mapInput(self, *args):
        """ Maps non keyworded arguments 
        
        Parameters:
            [email, password, first_name, last_name]
        """
        print(self.__class__.__name__, args)
        self.email = args[0]
        self.password = args[1]
        self.first_name = args[2]
        self.last_name = args[3]
        

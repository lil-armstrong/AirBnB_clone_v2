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
        [email, password, first_name, last_name]=args
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        

#!/usr/bin/python3
from models.base_model import BaseModel
"""User model module"""


class User(BaseModel):
    """user class definition
    Represent a user model object
    """
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""

    def mapInput(self, *args):
        """ Maps non keyworded arguments 

        Parameters:
            [email, password, first_name, last_name]
        """
        [email, password, first_name, last_name] = args
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

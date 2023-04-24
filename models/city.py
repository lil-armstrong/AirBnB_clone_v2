#!/usr/bin/python3
from models.base_model import BaseModel
from typing import Tuple, Union
"""City model module"""


class City(BaseModel):
    """City class definition
    Represent a City model object
    """
    name: str = ""
    state_id: str = ""

    def mapInput(self, args: Tuple[str, str]):
        """ Maps non keyworded arguments

        Parameters:
            args (Tuple[name:`str`,state_id:`str`]):\
                Tuple argument
        """
        [name, state_id] = args
        self.name = name
        self.state_id = state_id

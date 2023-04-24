#!/usr/bin/python3
from models.base_model import BaseModel
from typing import Tuple, Union
"""State model module"""


class State(BaseModel):
    """State class definition
    Represent a state model object
    """
    name: str = ""

    def mapInput(self, *args: str):
        """ Maps non keyworded arguments

        Parameters:
            args (Tuple[name:`str`]):\
                State attributes arguments

        Returns:
            None
        """

        [name] = args
        self.name = name

#!/usr/bin/python3
from models.base_model import BaseModel
from typing import Tuple
"""Review model module"""


class Review(BaseModel):
    """Review class definition
    Represent a Review model object
    """
    text: str = ""
    place_id: str = ""
    user_id: str = ""

    def mapInput(self, *args: str):
        """ Maps non keyworded arguments

        Parameters:
            args (Tuple[text:`str`, name:`str`, state_id:`str`]):\
                Review attribute list
        """
        (text, place_id, user_id) = args
        self.text = text
        self.place_id = place_id
        self.user_id = user_id

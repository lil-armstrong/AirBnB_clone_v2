#!/usr/bin/python3
from sqlalchemy import Column, ForeignKey, String

from models.base_model import BaseModel
from models.place import Place
from models.user import User

"""Review model module"""


class Review(BaseModel):
    """Review class definition
    Represent a Review model object
    """
    __tablename__ = "reviews"
    text = Column(String(128), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

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

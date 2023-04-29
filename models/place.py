#!/usr/bin/python3
from models.base_model import BaseModel, Base
from typing import Tuple, Union
"""Place model module"""


class Place(BaseModel):
    """Place class definition
    Represent a Place model object
    """
    name: str = ""
    city_id: str = ""
    user_id: str = ""
    max_guest: str = ""
    amenity_id: str = ""
    description: str = ""
    number_rooms: int = 0
    price_by_night: int = 0
    number_bathrooms: int = 0
    latitude: float = 0.0
    longitude: float = 0.0

    def mapInput(self, *args: Union[str, int, float]) -> None:
        """ Maps non keyworded arguments

        Parameters:
            *args (Tuple(Union[str,int,float]))): \
                Variable length of type int, str or float

        Returns:
            None
        """
        [name, city_id, user_id, amenity_id,
            description, number_bathrooms,
            number_rooms, max_guest,
            price_by_night, latitude, longitude] = args
        self.name = name
        self.user_id = user_id
        self.city_id = city_id
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.max_guest = int(max_guest)
        self.amenity_id = amenity_id
        self.description = description
        self.number_rooms = int(number_rooms)
        self.price_by_night = float(price_by_night)
        self.number_bathrooms = int(number_bathrooms)

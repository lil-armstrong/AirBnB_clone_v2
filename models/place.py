#!/usr/bin/python3
from typing import Tuple, Union

from sqlalchemy import Column, MetaData, Integer, Float, ForeignKey, String
from sqlalchemy.orm import backref, relationship

from models.base_model import Base, BaseModel
from models.city import City
from models.user import User
from models.amenity import Amenity

"""Place model module"""


class Place(BaseModel):
    """Place class definition
    Represent a Place model object
    """
    __tablename__ = "places"
    name = Column(String(128), unique=True, nullable=False)
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    amenity_id = Column(String(60), ForeignKey("amenities.id"), nullable=False)
    max_guest = Column(Integer, default=0)
    description = Column(String(128), nullable=False)
    number_rooms = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=False, default=0.0)
    longitude = Column(Float, nullable=False, default=0.0)
    user = relationship('User',
                        backref=backref('places',
                                        cascade='all, delete, delete-orphan'))
    city = relationship('City',
                        backref=backref('places',
                                        cascade='all, delete, delete-orphan'))
    amenity = relationship(
        'Amenity',
        backref=backref('places',
                        cascade='all, delete, delete-orphan'))

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

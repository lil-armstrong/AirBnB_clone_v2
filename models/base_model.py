#!/usr/bin/python3
import models
from uuid import uuid4
from datetime import datetime
import sys
"""Base Model"""


class BaseModel:
    """defines all common attributes/methods for other classes"""

    def __init__(self, *args, **kwargs):
        """Initializes the base class instance"""
        try:
            self.id = str(uuid4())
            self.created_at = datetime.today()
            self.updated_at = datetime.today()

            if (len(kwargs) != 0):
                for k, v in kwargs.items():
                    if k != "__class__":
                        if not hasattr(self, k):
                            raise AttributeError(
                                "Invalid attribute: [{}]".format(k))
                        attr_type = type(getattr(self, k))
                        if (k in ["created_at", "updated_at"]):
                            v = datetime.fromisoformat(v)
                        else:
                            v = attr_type(v)
                        setattr(self, k, v)
            else:
                self.mapInput(*args)
        except Exception as e:
            print(e, file=sys.stderr)
            pass
        else:
            models.storage.new(self)

    def mapInput(self, *args):
        """ Maps non keyworded arguments
        Can be overwritten to map individual arguments
        """
        pass

    def __str__(self):
        """Return string representation of the Base class"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__)

    def save(self):
        """Save the instance object"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        dict_obj = (self.__dict__).copy()
        dict_obj["__class__"] = self.__class__.__name__
        dict_obj["created_at"] = dict_obj["created_at"].isoformat()
        dict_obj["updated_at"] = dict_obj["updated_at"].isoformat()
        return dict_obj

    def update(self, name: str, value: str):
        """Updates the instance attribute"""
        try:
            if not hasattr(self, name):
                raise AttributeError(
                    "Invalid attribute: [{}]".format(name))
            attr_type = type(getattr(self, name))
            if (name in ["created_at", "updated_at"]):
                value = datetime.fromisoformat(value)
            else:
                value = attr_type(value)
            setattr(self, name, value)
        except Exception as e:
            print(e, file=sys.stderr)
            pass

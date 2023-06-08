#!/usr/bin/python3
import sys
from datetime import datetime
from os import getenv
from uuid import uuid4

import models

"""Base Model"""
from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

storage_type = getenv("HBNB_TYPE_STORAGE")
if storage_type == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel(Base):
    """defines all common attributes/methods for other classes"""
    __abstract__ = True
    id = Column(String(60), Sequence(name='id_seq'),
                primary_key=True, nullable=False, )
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    VALID_ATTR = {'id': str, 'created_at': type(datetime),
                  'updated_at': type(datetime)}

    def __init__(self, *args, **kwargs):
        """Initializes the base class instance"""
        try:
            if storage_type == 'db':
                super().__init__(**kwargs)
            self.validateInput(*args, **kwargs)
        except Exception as e:
            raise e

    def validateInput(self, *args, **kwargs):
        """Check arguments"""
        allowed_attrs = {**BaseModel.VALID_ATTR, **self.VALID_ATTR} or None
        attr_type = str
        kwargs_dict = kwargs.items()
        kwargs['id'] = kwargs.get('id', str(uuid4()))
        kwargs['created_at'] = datetime.fromisoformat(
            kwargs.get('created_at', datetime.today().isoformat()))
        kwargs['updated_at'] = datetime.fromisoformat(
            kwargs.get('updated_at', datetime.today().isoformat()))

        for attr, value in kwargs_dict:
            if attr not in ["__class__"]:
                attr_type = allowed_attrs[attr] or str
                if isinstance(type(value), attr_type) \
                        or type(value) is attr_type:
                    setattr(self, attr, value)
                else:
                    raise TypeError("Expected a %s for @%s. Got %s" % (
                        attr_type, attr, type(value)))
        if len(args):
            # if self.VALID_ATTR is not None \
            #         and len(args) < len(self.VALID_ATTR):
            #     raise ValueError("Invalid number of arguments passed")
            self.mapInput(*args)

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

    def __repr__(self):
        """return a string representaion
        """
        return self.__str__()

    def save(self, update=True):
        """Save the instance object"""
        if update:
            self.updated_at = datetime.today()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        dict_obj = (self.__dict__).copy()
        dict_obj["__class__"] = self.__class__.__name__

        if '_sa_instance_state' in dict_obj:
            del dict_obj['_sa_instance_state']

        if "created_at" in dict_obj:
            if isinstance(dict_obj["created_at"], datetime):
                dict_obj["created_at"] = dict_obj["created_at"].isoformat()
        if "updated_at" in dict_obj:
            if isinstance(dict_obj["updated_at"], datetime):
                dict_obj["updated_at"] = dict_obj["updated_at"].isoformat()

        return dict_obj

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)

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

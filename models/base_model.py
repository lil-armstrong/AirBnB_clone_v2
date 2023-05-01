#!/usr/bin/python3
import models
from uuid import uuid4
from datetime import datetime
import sys
"""Base Model"""
from sqlalchemy import (Column, String, Integer, DateTime, Sequence)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """defines all common attributes/methods for other classes"""
    __abstract__ = True
    id = Column(String(60), Sequence(name='id_seq'),
                primary_key=True, nullable=False, )
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initializes the base class instance"""
        try:
            # super().__init__(**kwargs)
            self.validator(*args, **kwargs)
        except Exception as e:
            raise e

    def validator(self, *args, **kwargs):
        """Check arguments"""
        allowed_attrs = self.VALID_ATTR or None
        attr_type = str

        if args:
            if allowed_attrs is not None \
                    and len(args) != len(allowed_attrs):
                raise ValueError("Invalid number of arguments passed")
            self.mapInput(*args)
        elif kwargs:
            kwargs_dict = kwargs.items()
            if allowed_attrs is not None:
                allowed_attrs_len = len(allowed_attrs)
                for k in ["id", "created_at", "updated_at", "__class__"]:
                    if k in kwargs:
                        allowed_attrs_len += 1

                if len(kwargs_dict) != allowed_attrs_len:
                    raise ValueError("Invalid number of arguments")

            if 'id' not in kwargs:
                kwargs['id'] = str(uuid4())
            if 'created_at' not in kwargs:
                kwargs['created_at'] = datetime.utcnow()
            else:
                kwargs['created_at'] = datetime.fromisoformat(
                    kwargs['created_at'])

            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = datetime.utcnow()
            else:
                kwargs['created_at'] = datetime.fromisoformat(
                    kwargs['updated_at'])
            for attr, value in kwargs_dict:
                if attr not in ["__class__"]:
                    if allowed_attrs and attr in allowed_attrs:
                        attr_type = allowed_attrs[attr]
                    else:
                        attr_type = str

                    if attr not in ["created_at", "updated_at"]:
                        value = attr_type(value)

                    setattr(self, attr, value)

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

    def save(self):
        """Save the instance object"""
        models.storage.new(self)
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        dict_obj = (self.__dict__).copy()
        if '_sa_instance_state' in dict_obj:
            del dict_obj['_sa_instance_state']

        dict_obj["__class__"] = self.__class__.__name__
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

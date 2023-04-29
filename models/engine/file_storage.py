#!/usr/bin/python3
import json
import os

from models import base_model
from models.state import State
from models.city import City
# from models import place
# from models import review
# from models import user
# from models import amenity

BaseModel = base_model.BaseModel

"""FileStorage serializes class instances to a JSON file
and deserializes JSON file to instances"""


class FileStorage:
    """FileStorage class"""
    __file_path = "file.json"
    __objects = {}

    @property
    def filePath(self):
        """Return the file path"""
        return FileStorage.__file_path

    def all(self, cls: BaseModel = None):
        """Returns the dictionary __objects"""

        stored = FileStorage.__objects
        if cls is not None:
            result = dict()
            for obj in stored:
                if stored[obj].__class__.__name__ == cls.__name__:
                    result[obj] = stored[obj]
            return result
        return stored

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""

        key = FileStorage.makeKey(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj
        return obj

    def delete(self, obj: BaseModel = None):
        """Removes a key from the __objects"""
        objs = FileStorage.__objects
        if obj is not None:
            # Checks if the key exist
            key = FileStorage.makeKey(obj.__class__.__name__, obj.id)
            if key in objs:
                del objs[key]

        return objs

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(self.filePath, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.exists(self.filePath):
            with open(self.filePath, "r") as fp:
                # deserialize json file to __objects
                serialized = json.load(fp)

                for v in serialized.values():

                    cls_name = v["__class__"]
                    cls = eval(cls_name)
                    self.new(cls(**v))

    @staticmethod
    def makeKey(cls_name, id: str):
        """Generates a storage key using the class name and id"""
        return "{}.{}".format(cls_name, id)

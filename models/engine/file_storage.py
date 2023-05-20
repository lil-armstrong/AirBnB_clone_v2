#!/usr/bin/python3
import json
import os
from typing import Dict, Optional, Type

from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class FileStorage:
    __file_path = "file.json"
    __objects: Dict[str, BaseModel] = {}

    @property
    def filePath(self) -> str:
        return self.__file_path

    def all(self, cls: Optional[Type[BaseModel]] = None) -> Dict[str, BaseModel]:
        stored = self.__objects
        if cls is not None:
            return {obj_id: obj for obj_id, obj in stored.items() if isinstance(obj, cls)}
        return stored

    def new(self, obj: BaseModel) -> BaseModel:
        key = self.makeKey(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj
        return obj

    def delete(self, obj: Optional[BaseModel] = None):
        if obj is not None:
            key = self.makeKey(obj.__class__.__name__, obj.id)
            self.__objects.pop(key, None)

    def save(self):
        obj_dict = {obj_id: obj.to_dict() for obj_id, obj in self.__objects.items()}
        with open(self.filePath, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        if os.path.exists(self.filePath):
            with open(self.filePath, "r") as fp:
                serialized = json.load(fp)
                for obj_data in serialized.values():
                    cls_name = obj_data["__class__"]
                    cls = eval(cls_name)
                    self.new(cls(**obj_data))

    @staticmethod
    def makeKey(cls_name: str, obj_id: str) -> str:
        return f"{cls_name}.{obj_id}"

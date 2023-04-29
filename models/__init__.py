#!/usr/bin/python3
import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

"""__init__ magic method for models directory"""

env = os.environ

storage_type = env.get("HBNB_TYPE_STORAGE")

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
__all__ = ["base_model", "console", "storage",
           "user", "amenity", "city", "place", "state", "review"]

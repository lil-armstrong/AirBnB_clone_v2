#!/usr/bin/env python3
# Tests the BaseModel class


import models
from models.base_model import BaseModel

if __name__ == "__main__":

    all_objs = models.storage.all()
    print(all_objs)
    print("--Create new object--")
    my_model = BaseModel()
    my_model.save()
    print(my_model)

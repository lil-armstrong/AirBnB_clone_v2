#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

        env = os.getenv
        user = env("HBNB_MYSQL_USER")
        password = env("HBNB_MYSQL_PWD")
        db = env("HBNB_MYSQL_DB")
        port = 3306
        host = env("HBNB_MYSQL_HOST")
        env = env("HBNB_ENV")
        is_test = env == 'test'

        engine = create_engine(
            'mysql+mysqldb://{}:{}@{}:{}/{}'
            .format(
                user,
                password,
                host,
                port,
                db
            ),
            pool_pre_ping=True,
            # echo=True
        )

        metadata = Base.metadata
        metadata.bind = engine

        if is_test:
            # drop all tables if is test
            metadata.drop_all()

        self.__engine = engine
        self.__metadata = metadata

    def all(self, cls: BaseModel = None):
        """query on the current database session\
all objects depending of the class name (argument cls)
        """
        inspector = inspect(self.__engine)
        tables = inspector.get_table_names()
        result = dict()
        from_db = {}
        class_name = cls
        key = None
        session = self.__session

        if cls is None and tables is not None:
            # Query everything
            for table in tables:
                if table in table_class_map:
                    cls = eval(table_class_map[table])
                    from_db[class_name] = session.query(
                        cls).all()

        else:
            from_db[class_name] = session.query(
                cls).all()

        for k in from_db.keys():
            for data in from_db[k]:
                key = DBStorage.makeKey(k, data.id)
                result[key] = data
        return result

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

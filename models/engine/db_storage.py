import os
from typing import Type

from sqlalchemy import MetaData, create_engine, inspect, text, Table
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from models.base_model import BaseModel
from models.base_model import Base
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User

"""Database storage engine"""


table_class_map = {
    "cities": 'City',
    "states": "State",
    "places": "Place",
    "amenities": "Amenity",
    "reviews": "Review",
}


class DBStorage:
    """Database storage engine"""

    __engine = None
    __metadata = None
    __session = None

    def __init__(self):
        """Initializing database storage engine"""

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
        self.reload()

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
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session `obj` if not `None`"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        if self.__session is not None:
            self.__session.close_all()
        self.__metadata.create_all()
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    @staticmethod
    def makeKey(cls_name, id: str):
        """Generates a storage key using the class name and id"""
        return "{}.{}".format(cls_name, id)

import os
from typing import Type

from sqlalchemy import MetaData, create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from models.base_model import BaseModel
from models.city import City
from models.state import State

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

    def __init__(self):
        """Initializing database storage engine"""
        self.__engine = None
        self.__metadata = None
        self.__session = None

        env = os.environ
        user = env.get("HBNB_MYSQL_USER")
        password = env.get("HBNB_MYSQL_PWD")
        db = env.get("HBNB_MYSQL_DB")
        port = 3306
        host = env.get("HBNB_MYSQL_HOST")
        env = env.get("HBNB_ENV")
        is_test = env == 'test'

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}:{}/{}'
            .format(
                user,
                password,
                host,
                port,
                db
            ),
            pool_pre_ping=True)

        self.__metadata = MetaData(
            bind=self.__engine, schema=BaseModel.metadata)

        if is_test:
            # drop all tables if is test
            self.metadata.drop_all()

    def all(self, cls=None):
        """query on the current database session\
all objects depending of the class name (argument cls)
        """
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        result = dict()
        from_db = {}
        class_name = cls
        key = None

        if cls is None and tables is not None:
            # Query everything
            for table in tables:
                if table in table_class_map:
                    class_name = table_class_map[table]
                    from_db[class_name] = self.session.query(class_name).all()

        else:
            from_db[class_name] = self.session.query(class_name).all()

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
        self.__metadata.create_all(checkfirst=True)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    @staticmethod
    def makeKey(cls_name, id: str):
        """Generates a storage key using the class name and id"""
        return "{}.{}".format(cls_name, id)

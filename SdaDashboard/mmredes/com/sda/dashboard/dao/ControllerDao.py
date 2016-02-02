from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

__author__ = 'macbook'
Base = automap_base()

class ControllerDao:
    _db_engine = None
    _session = None
    _dict_database = {}

    def __init__(self, db_path):
        connection_str = "sqlite:///%s" % db_path
        self._db_engine = create_engine(connection_str)

        # reflect the tables
        Base.prepare(self._db_engine, reflect=True)
        # create a session
        Session = sessionmaker(bind=self._db_engine)
        self._session = Session()

        self._dict_database["engine"] = self._db_engine
        self._dict_database["base"] = Base
        self._dict_database["session"] = self._session



    def get_dict_database(self):
        return self._dict_database
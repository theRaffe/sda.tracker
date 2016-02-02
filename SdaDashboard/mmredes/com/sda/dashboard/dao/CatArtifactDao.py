from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

__author__ = 'macbook'


class CatArtifactDao:
    _db_engine = None
    _metadata = None

    def __init__(self, dict_database):
        self._db_engine = dict_database["engine"]
        self._session = dict_database["session"]
        self._Base = dict_database["base"]
        self._cat_artifacts = self._Base.classes.cat_artifact

    def list_all(self):
        return self._session.query(self._cat_artifacts).all()

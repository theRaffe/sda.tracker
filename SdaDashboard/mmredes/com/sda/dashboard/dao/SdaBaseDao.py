__author__ = 'macbook'

class SdaBaseDao:
    _db_engine = None
    _metadata = None
    _Base = None
    _session =  None

    def __init__(self, dict_database):
        self._db_engine = dict_database["engine"]
        self._session = dict_database["session"]
        self._Base = dict_database["base"]

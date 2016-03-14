import logging
import cherrypy
from mmredes.com.sda.dashboard.dao.CatArtifactDao import CatArtifactDao

__author__ = 'macbook'
logger = logging.getLogger(__name__)

class DashBoardRoot(object):

    _dict_database = {}

    def __init__(self, schema_base):
        logger.info('Base object %s' % schema_base)
        self._dict_database["engine"] = cherrypy.engine
        self._dict_database["base"] = schema_base
#        self._dict_database["session"] = cherrypy.request.db

    def index(self):
        self._dict_database["session"] = cherrypy.request.db
        """
        List users from the DB & add new if no users
        """
        cat_artifact_dao = CatArtifactDao(self._dict_database)
        artifacts = cat_artifact_dao.list_all()
        return 'artifacts: %s' % (artifacts)
    index.exposed = True


    def get_dict_database(self):
        #Base.prepare(cherrypy.engine, reflect=True)
        self._dict_database["engine"] = cherrypy.engine
        #self._dict_database["base"] = Base
        self._dict_database["session"] = cherrypy.request.db

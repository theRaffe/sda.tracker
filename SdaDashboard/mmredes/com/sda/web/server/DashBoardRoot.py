import logging
from cherrypy import log

import cherrypy

from mmredes.com.sda.dashboard.PersistentController import PersistentController
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

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def process_ticket(self, **kwargs):
        self._dict_database["session"] = cherrypy.request.db
        input_json = cherrypy.request.json

        persistent_controller = PersistentController(dict_database=self._dict_database)
        json_result = persistent_controller.process_ticket_artifact(input_json)

        return json_result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def process_ticket_library(self, **kwargs):
        self._dict_database["session"] = cherrypy.request.db
        input_json = cherrypy.request.json

        persistent_controller = PersistentController(dict_database=self._dict_database)
        return persistent_controller.process_library_ticket(input_json)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def linking_tickets(self, **kwargs):
        self._dict_database["session"] = cherrypy.request.db
        input_json = cherrypy.request.json

        persistent_controller = PersistentController(dict_database=self._dict_database)
        return persistent_controller.linking_tickets(input_json)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def update_status_ticket(self, **kwargs):
        self._dict_database["session"] = cherrypy.request.db
        input_json = cherrypy.request.json

        persistent_controller = PersistentController(dict_database=self._dict_database)
        return persistent_controller.update_status_ticket(input_json)

    @cherrypy.expose
    def shutdown(self):
        cherrypy.engine.exit()

    def get_dict_database(self):
        # Base.prepare(cherrypy.engine, reflect=True)
        self._dict_database["engine"] = cherrypy.engine
        # self._dict_database["base"] = Base
        self._dict_database["session"] = cherrypy.request.db

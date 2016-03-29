import json
import time
from mmredes.com.sda.dashboard.dao.CatArtifactDao import CatArtifactDao
from mmredes.com.sda.dashboard.dao.CatBranchDao import CatBranchDao
from mmredes.com.sda.dashboard.dao.ControllerDao import ControllerDao
from mmredes.com.sda.dashboard.dao.TicketArtifactDao import TicketArtifactDao
from mmredes.com.sda.dashboard.dao.TicketArtifactLoggingDao import TicketArtifactLoggingDao
from mmredes.com.sda.dashboard.dao.TicketBoardDao import TicketBoardDao
from mmredes.com.sda.dashboard.dao.TicketLibraryDao import TicketLibraryDao
from mmredes.com.sda.utils import ConfigLogger
from sqlalchemy.ext.declarative import DeclarativeMeta

__author__ = 'macbook'
import sqlite3 as lite
import ConfigParser
import logging

from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao

ConfigLogger.get_sda_logger()
logger = logging.getLogger(__name__)


class PersistentController:
    dao_object = None
    _controller_dao = None

    def __init__(self, config_file=None, dict_database = None):

        if dict_database:
            self._controller_dao = ControllerDao(dict_database = dict_database)
        else:
            logger.info("config_file: %s" % config_file)
            config = ConfigParser.RawConfigParser()
            config.read(config_file)
            connection_file = config.get('DatabaseSection', 'database.file')
            self.dao_object = SdaTrackerDao(connection_file)
            self._controller_dao = ControllerDao(connection_file)

    def get_artifacts(self):
        cat_artifact_dao = CatArtifactDao(self._controller_dao.get_dict_database())
        rows = cat_artifact_dao.list_all()
        dict_artifact = {}
        for row in rows:
            key = row.path_directory
            value_key = row.id_artifact
            dict_artifact[key] = value_key
        return dict_artifact

    def get_list_artifacts(self):
        cat_artifact_dao = CatArtifactDao(self._controller_dao.get_dict_database())
        return cat_artifact_dao.list_all()

    def get_ticket_board(self, ticket):
        ticket_board_dao = TicketBoardDao(self._controller_dao.get_dict_database())
        row = ticket_board_dao.get_ticket(ticket)
        return row

    def get_ticket_artifact(self, id_ticket, id_artifact, type_tech):
        ticket_artifact_dao = TicketArtifactDao(self._controller_dao.get_dict_database())
        row = ticket_artifact_dao.get_ticket_artifact(id_ticket, id_artifact, type_tech)
        return row

    def get_dict_board_code(self, id_ticket):
        ticket_board_dao = TicketBoardDao(self._controller_dao.get_dict_database())
        ticket_artifact_dao = TicketArtifactDao(self._controller_dao.get_dict_database())
        row_board_code = ticket_board_dao.get_ticket_code(id_ticket)
        rows = ticket_artifact_dao.get_ticket_artifact_code(id_ticket)

        list_artifact = []
        for a_row in rows:
            list_artifact.append(json.dumps(a_row, cls=AlchemyEncoder))

        return {"dict_board": json.dumps(row_board_code, cls=AlchemyEncoder), "artifacts": list_artifact}

    def insert_ticket_board(self, dic_ticket_board):
        ticket_board_dao = TicketBoardDao(self._controller_dao.get_dict_database())
        ticket_board_dao.add(dic_ticket_board)

    def get_ticket_environment(self, id_ticket, id_branch = None):
        ticket_library_dao = TicketLibraryDao(self._controller_dao.get_dict_database())
        id_environment = ticket_library_dao.get_id_environment(id_ticket)
        if id_environment:
            return id_environment

        cat_branch_dao = CatBranchDao(self._controller_dao.get_dict_database())
        return cat_branch_dao.get_environment(1)

    def do_commit(self):
        self._controller_dao.do_commit()

    def close_session(self):
        self._controller_dao.close_session()
        self._controller_dao._session.close_all()

    def process_ticket_db(self, dict_branch, id_branch_rep):
        list_board_ticket = []
        try:
            for id_ticket in dict_branch:

                ls_artifact = dict_branch[id_ticket]
                if len(ls_artifact) > 0:
                    logger.debug("search ticket %s" % id_ticket)
                    row_ticket_board = self.get_ticket_board(id_ticket)
                    # if ticket exists
                    if row_ticket_board:
                        # get first dict artifact
                        first_artifact = ls_artifact[0]
                        user_request = first_artifact["email"]
                        # update user_request with new value of the artifact's email
                        row_ticket_board.user_request = user_request
                        row_ticket_board.date_requested = time.time()
                        logger.info("update ticket_board.date_requested")
                        # print "search ticket_artifact by id_artifact, type_tech"
                    else:
                        first_artifact = ls_artifact[0]
                        user_request = first_artifact["email"]
                        id_environment = self.get_ticket_environment(id_ticket=id_ticket, id_branch=id_branch_rep)
                        dict_ticket = {"id_ticket": id_ticket, "id_environment": id_environment,
                                       "user_request": user_request}
                        print "creating ticket_board, id_environment, id_ticket, id_status, date_requested..."
                        self.insert_ticket_board(dict_ticket)

                    ticket_artifact_dao = TicketArtifactDao(self._controller_dao.get_dict_database())
                    ticket_artifact_logging = TicketArtifactLoggingDao(self._controller_dao.get_dict_database())
                    for dict_artifact in ls_artifact:
                        ticket_artifact_dao.process_ticket_artifact(id_ticket, dict_artifact)
                        ticket_artifact_logging.add(id_ticket, dict_artifact)

                    board_ticket = self.get_dict_board_code(id_ticket)
                    list_board_ticket.append(board_ticket)

            self.do_commit()
            return {"result": "OK", "board_ticket": list_board_ticket}
        except lite.Error as e:
            logger.exception(e)
            self._controller_dao.do_rollback()
            return {"result": "ERROR", "description": e.message}


    def process_ticket_artifact(self, dict_ticket_artifact):
        id_ticket = dict_ticket_artifact["id_ticket"]
        logger.debug("search ticket %s" % id_ticket)
        row_ticket_board = self.get_ticket_board(id_ticket)
        # if ticket exists
        if row_ticket_board:
            user_request = dict_ticket_artifact["modification_user"]
            # update user_request with new value of the artifact's email
            row_ticket_board.user_request = user_request
            row_ticket_board.date_requested = time.time()

        else:
            user_request = dict_ticket_artifact["modification_user"]
            id_environment = self.get_ticket_environment(id_ticket=id_ticket)
            dict_ticket = {"id_ticket": id_ticket, "id_environment": id_environment,
                           "user_request": user_request}
            print "creating ticket_board, id_environment, id_ticket, id_status, date_requested..."
            self.insert_ticket_board(dict_ticket)

        ticket_artifact_dao = TicketArtifactDao(self._controller_dao.get_dict_database())
        ticket_artifact_logging = TicketArtifactLoggingDao(self._controller_dao.get_dict_database())
        cat_artifact_dao = CatArtifactDao(self._controller_dao.get_dict_database())

        ls_artifact = dict_ticket_artifact["artifacts"]
        for code_artifact in ls_artifact:
            id_artifact = cat_artifact_dao.get_id_artifact(code_artifact)

            ticket_artifact_dao.process_ticket_artifact(id_artifact, dict_ticket_artifact)
            ticket_artifact_logging.add(id_artifact, dict_ticket_artifact)

        board_ticket = self.get_dict_board_code(id_ticket)
        return {"result": "OK", "board_ticket": board_ticket}


    def update_ticket_db(self, dict_board_ticket):
        self.dao_object.update_ticket_board(dict_board_ticket)
        return None

    def process_library_ticket(self, dict_defect):
        id_environment = self.dao_object.translate_environment(dict_defect)
        if id_environment:
            id_ticket = dict_defect["id_defect"]
            description = dict_defect["description"][:200]
            dict_ticket = {"id_ticket": id_ticket, "id_environment": id_environment, "description": description}
            self.dao_object.add_upd_library_ticket(dict_ticket)
            self.dao_object.do_commit()
        else:
            logger.error("couldn't find id_environment, with crm=%s environment=%s" % (
                dict_defect["crm"], dict_defect["environment"]))


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
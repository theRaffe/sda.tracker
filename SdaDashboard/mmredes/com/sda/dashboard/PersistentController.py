import json
import time
from mmredes.com.sda.dashboard.dao.CatArtifactDao import CatArtifactDao
from mmredes.com.sda.dashboard.dao.CatBranchDao import CatBranchDao
from mmredes.com.sda.dashboard.dao.CatEnvironmentDao import CatEnvironmentDao
from mmredes.com.sda.dashboard.dao.ControllerDao import ControllerDao
from mmredes.com.sda.dashboard.dao.TicketArtifactDao import TicketArtifactDao
from mmredes.com.sda.dashboard.dao.TicketArtifactLoggingDao import TicketArtifactLoggingDao
from mmredes.com.sda.dashboard.dao.TicketBoardDao import TicketBoardDao
from mmredes.com.sda.dashboard.dao.TicketLibraryDao import TicketLibraryDao
from mmredes.com.sda.dashboard.dao.TranslateEnvironmentDao import TranslateEnvironmentDao
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

    def __init__(self, config_file=None, dict_database=None):

        if dict_database:
            self._controller_dao = ControllerDao(dict_database=dict_database)
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

    def get_ticket_board(self, id_ticket):
        ticket_board_dao = TicketBoardDao(self._controller_dao.get_dict_database())
        row = ticket_board_dao.get_ticket(id_ticket)
        return row

    def get_ticket_artifact(self, id_ticket, id_artifact, type_tech):
        ticket_artifact_dao = TicketArtifactDao(self._controller_dao.get_dict_database())
        row = ticket_artifact_dao.get_ticket_artifact(id_ticket, id_artifact, type_tech)
        return row

    def get_all_ticket_artifact(self, id_ticket):
        ticket_artifact_dao = TicketArtifactDao(self._controller_dao.get_dict_database())
        return ticket_artifact_dao.get_all_ticket_artifact(id_ticket)

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

    def get_ticket_environment(self, id_ticket, id_branch=None):
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
        dict_ticket_artifact["code_base"] = id_ticket
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
        translate_environment_dao = TranslateEnvironmentDao(self._controller_dao.get_dict_database())
        crm = dict_defect["crm"]
        environment = dict_defect["environment"]

        id_environment = translate_environment_dao.translate(crm=crm, environment=environment)
        if id_environment:
            id_ticket = dict_defect["id_ticket"]
            description = dict_defect["description"][:200]

            dict_ticket = {"id_ticket": id_ticket, "id_environment": id_environment, "description": description,
                           "id_requirement": dict_defect["id_requirement"], "id_release": dict_defect["id_release"]}

            ticket_library_dao = TicketLibraryDao(self._controller_dao.get_dict_database())
            ticket_library_dao.process_ticket_library(dict_ticket)

            ticket_board_dao = TicketBoardDao(self._controller_dao.get_dict_database())
            ticket_board_dao.update_environment(id_ticket, id_environment)
            return {"result_code": "OK", "message": "success"}
        else:
            message_error = "couldn't find id_environment at translate_environment table, with crm=%s environment=%s" % (
                dict_defect["crm"], dict_defect["environment"])
            logger.error(message_error)
            return {"result_code": "ERROR", "message": message_error}

    def linking_tickets(self, dict_link_ticket):
        id_ticket_original = dict_link_ticket["id_ticket_original"]
        id_ticket_linked = dict_link_ticket["id_ticket_linked"]
        row_ticket_board = self.get_ticket_board(id_ticket_original)
        row_ticket_linked = self.get_ticket_board(id_ticket_linked)

        if not row_ticket_board:
            return {"result_code": "ERROR", "message": "original ticket doesn't exist!"}

        if row_ticket_linked:
            return {"result_code": "ERROR", "message": "linked ticket already exists"}
        else:
            rows_ticket_artifact = self.get_all_ticket_artifact(id_ticket_original)
            user_request = row_ticket_board.user_request
            id_environment = row_ticket_board.id_environment
            dict_ticket = {"id_ticket": id_ticket_linked, "id_environment": id_environment,
                           "user_request": user_request}
            self.insert_ticket_board(dict_ticket)
            ticket_artifact_dao = TicketArtifactDao(self._controller_dao.get_dict_database())
            # copy original ticket's artifacts to the new ticket
            for row in rows_ticket_artifact:
                dict_ticket_artifact = {"id_ticket": id_ticket_linked, "id_type_tech": row.id_type_tech,
                                        "modification_user": row.modification_user,
                                        "id_revision": row.id_revision, "build_release": row.build_release,
                                        "build_hotfix": row.build_hotfix}
                ticket_artifact_dao.process_ticket_artifact(id_artifact=row.id_artifact,
                                                            dict_artifact=dict_ticket_artifact)

            return {"result_code": "OK", "message": "success"}

    def update_status_ticket(self, dict_status_ticket):
        ticket_board_dao = TicketBoardDao(self._controller_dao.get_dict_database())
        row = ticket_board_dao.update_status(dict_status_ticket)

        if row:
            return {"result_code": "OK", "message": "success"}

        return {"result_code": "ERROR", "message": "ticket not found with id %s" % dict_status_ticket['id_ticket']}


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

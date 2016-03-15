import time
from mmredes.com.sda.dashboard.dao.CatArtifactDao import CatArtifactDao
from mmredes.com.sda.dashboard.dao.CatBranchDao import CatBranchDao
from mmredes.com.sda.dashboard.dao.ControllerDao import ControllerDao
from mmredes.com.sda.dashboard.dao.TicketArtifactDao import TicketArtifactDao
from mmredes.com.sda.dashboard.dao.TicketArtifactLoggingDao import TicketArtifactLoggingDao
from mmredes.com.sda.dashboard.dao.TicketBoardDao import TicketBoardDao
from mmredes.com.sda.dashboard.dao.TicketLibraryDao import TicketLibraryDao
from mmredes.com.sda.utils import ConfigLogger

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

    def __init__(self, config_file="./board.cfg"):
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

        return {"dict_board": row_board_code, "artifacts": rows}

    def insert_ticket_board(self, dic_ticket_board):
        ticket_board_dao = TicketBoardDao(self._controller_dao.get_dict_database())
        ticket_board_dao.add(dic_ticket_board)

    def get_ticket_environment(self, id_ticket, id_branch):
        ticket_library_dao = TicketLibraryDao(self._controller_dao.get_dict_database())
        id_environment = ticket_library_dao.get_id_environment(id_ticket)
        if id_environment:
            return id_environment

        cat_branch_dao = CatBranchDao(self._controller_dao.get_dict_database())
        return cat_branch_dao.get_environment(id_branch)

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

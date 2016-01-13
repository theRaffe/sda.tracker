__author__ = 'macbook'
import sqlite3 as lite
import ConfigParser
import logging

from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PersistentController:
    dao_object = None

    def __init__(self, config_file="./board.cfg"):
        logger.info("config_file: %s" % config_file)
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        self.dao_object = SdaTrackerDao(connection_file)

    def get_artifacts(self):
        return self.dao_object.get_artifacts()

    def get_list_artifacts(self):
        return self.dao_object.get_list_artifacts()

    def get_ticket_board(self, ticket):
        row = self.dao_object.get_ticket(ticket)
        if row:
            return dict(zip(row.keys(), row))
        else:
            return None

    def get_ticket_artifact(self, id_ticket, id_artifact, type_tech):
        row = self.dao_object.get_ticket_artifact(id_ticket, id_artifact, type_tech)
        if row:
            return dict(zip(row.keys(), row))
        else:
            return None

    def get_dict_board_code(self, id_ticket):
        row_board_code = self.dao_object.get_ticket_board_code(id_ticket)
        dict_board_code = dict(zip(row_board_code.keys(), row_board_code))

        rows = self.dao_object.get_artifact_code(id_ticket)
        list_artifact = []
        for row in rows:
            dict_artifact = dict(zip(row.keys(), row))
            list_artifact.append(dict_artifact)

        return {"dict_board": dict_board_code, "artifacts": list_artifact}

    def process_ticket_db(self, dict_branch, id_branch_rep):
        list_board_ticket = []
        try:
            for id_ticket in dict_branch:
                print "search ticket %s" % id_ticket
                dict_ticket = self.get_ticket_board(id_ticket)
                ls_artifact = dict_branch[id_ticket]
                if dict_ticket and len(ls_artifact) > 0:
                    # get first dict artifact
                    first_artifact = ls_artifact[0]
                    user_request = first_artifact["email"]
                    # update user_request with new value of the artifact's email
                    dict_ticket["user_request"] = user_request
                    logger.info("update ticket_board.date_requested")
                    self.dao_object.update_ticket_board(dict_ticket)
                    # print "search ticket_artifact by id_artifact, type_tech"

                    for dict_artifact in ls_artifact:
                        id_artifact = dict_artifact["id_artifact"]
                        id_type_tech = dict_artifact["id_type_tech"]
                        row_ticket_artifact = self.get_ticket_artifact(id_ticket, id_artifact, id_type_tech)
                        if row_ticket_artifact:
                            self.dao_object.update_ticket_artifact(id_ticket, dict_artifact)
                            # print "update ticket_artifact.modified_date, ticket_artifact.modifier_email"
                        else:
                            self.dao_object.insert_ticket_artifact(id_ticket, dict_artifact)
                            # print "create artifact id_artifact, type_tech, creator_email, creation_date"

                        self.dao_object.insert_ticket_logging(id_ticket, dict_artifact)
                else:
                    first_artifact = ls_artifact[0]
                    user_request = first_artifact["email"]
                    id_environment = self.dao_object.get_default_environment(id_branch_rep)
                    dict_ticket = {"id_ticket": id_ticket, "id_environment": id_environment,
                                   "user_request": user_request}
                    print "creating ticket_board, id_environment, id_ticket, id_status, date_requested..."
                    self.dao_object.insert_ticket_board(dict_ticket)
                    print "create ticket_board, id_environment, id_ticket, id_status, date_requested"
                    for dict_artifact in ls_artifact:
                        self.dao_object.insert_ticket_logging(id_ticket, dict_artifact)
                        self.dao_object.insert_ticket_artifact(id_ticket, dict_artifact)
                    print "create ticket_artifact id_ticket, id_artifact, creator_email, creation_date"
                board_ticket = self.get_dict_board_code(id_ticket)
                list_board_ticket.append(board_ticket)

            self.dao_object.do_commit()
            return {"result": "OK", "board_ticket": list_board_ticket}
        except lite.Error, e:
            print "Error Database %s:" % e.args
            logger.exception(e)

            self.dao_object.do_rollback()
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

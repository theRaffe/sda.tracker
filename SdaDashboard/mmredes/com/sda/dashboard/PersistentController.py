__author__ = 'macbook'
from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao
import sqlite3 as lite
import ConfigParser


class PersistentController:
    dao_object = None

    def __init__(self, config_file = "./board.cfg"):
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

    def get_dict_ticket_code(self, dict_ticket):
        id_ticket = dict_ticket["id_ticket"]
        dict_ticket_board = self.dao_object.get_ticket_board_code(id_ticket)

        #dao_object.
        return None

    def process_ticket_db(self, dict_branch, id_branch_rep):
        try:
            for id_ticket in dict_branch:
                print "search ticket %s" % id_ticket
                dict_ticket = self.get_ticket_board(id_ticket)
                ls_artifact = dict_branch[id_ticket]
                if dict_ticket:
                    print "update ticket_board.date_requested"
                    self.dao_object.update_ticket_board(dict_ticket)
                    print "search ticket_artifact by id_artifact, type_tech"

                    for dict_artifact in ls_artifact:
                        id_artifact = dict_artifact["id_artifact"]
                        id_type_tech = dict_artifact["id_type_tech"]
                        row_ticket_artifact = self.get_ticket_artifact(id_ticket, id_artifact, id_type_tech)
                        if row_ticket_artifact:
                            self.dao_object.update_ticket_artifact(id_ticket, dict_artifact)
                            print "update ticket_artifact.modified_date, ticket_artifact.modifier_email"
                        else:
                            self.dao_object.insert_ticket_artifact(id_ticket, dict_artifact)
                            print "create artifact id_artifact, type_tech, creator_email, creation_date"
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
                        self.dao_object.insert_ticket_artifact(id_ticket, dict_artifact)
                    print "create ticket_artifact id_ticket, id_artifact, creator_email, creation_date"


            self.dao_object.do_commit()
        except lite.Error, e:
            print "Error Database %s:" % e.args
            self.dao_object.do_rollback()


__author__ = 'macbook'
from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao


class DriverDao:
    dao_object = None
    connection_file = '/Users/macbook/Documents/workspaces/python/sda_tracker_workspace/sda.tracker/db.sda.tracker/sda_tracking.db'

    def __init__(self):
        self.dao_object = SdaTrackerDao(self.connection_file)

    def get_artifacts(self):
        return self.dao_object.get_artifacts()

    def get_ticket_board(self, ticket):
        return self.dao_object.get_ticket(ticket)

    def get_ticket_artifact(self, ticket, id_artifact, type_tech):
        return None

    def manage_ticket_db(self, dict_branch):
        for ticket in dict_branch:
            print "search ticket"
            ticket_row = self.get_ticket_board(ticket)

            if ticket_row:
                ls_artifact = dict_branch[ticket]
                print "update ticket_board.date_requested"
                print "search ticket_artifact by id_artifact, type_tech"

                for dict_artifact in ls_artifact:
                    id_artifact = dict_artifact["id_artifact"]
                    id_type_tech = dict_artifact["type_tech"]
                    row_ticket_artifact = self.get_ticket_artifact(ticket, id_artifact, id_type_tech)
                    if row_ticket_artifact:
                        print "update ticket_artifact.modified_date, ticket_artifact.modifier_email"
                    else:
                        print "create artifact id_artifact, type_tech, creator_email, creation_date"
            else:
                print "create ticket_board, id_environment, id_ticket, id_status, date_requested"
                print "create ticket_artifact id_ticket, id_artifact, creator_email, creation_date"


driver = DriverDao()
print driver.get_artifacts()

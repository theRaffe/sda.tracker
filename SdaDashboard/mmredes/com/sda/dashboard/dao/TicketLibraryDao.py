import time
from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'

class TicketLibraryDao(SdaBaseDao):

    def process_ticket_library(self, dict_ticket):
        Base = self._Base
        date_current = time.time()
        id_ticket = dict_ticket["id_ticket"]
        id_environment = dict_ticket["id_environment"]
        description = dict_ticket["description"]

        TicketLibrary = Base.classes.ticket_library

        row = self._session.query(TicketLibrary).filter(TicketLibrary.id_ticket == id_ticket)
        if row:
            row.id_environment = id_environment
            row.description = description
        else:
            row = TicketLibrary(id_ticket = id_ticket, id_environment = id_environment, description = description, creation_date = date_current)
            self._session.add(row)
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
        id_requirement = dict_ticket["id_requirement"]
        id_release = dict_ticket["id_release"]
        user_detect = dict_ticket['user_detect']
        id_type_defect = dict_ticket['id_type_defect']
        user_assign = dict_ticket['user_assign']

        TicketLibrary = Base.classes.ticket_library

        rows = self._session.query(TicketLibrary).filter(TicketLibrary.id_ticket == id_ticket).all()
        if len(rows) > 0:
            row = rows[0]
            row.id_environment = id_environment
            row.description = description
            row.id_requirement = id_requirement
            row.id_release = id_release
            row.user_detect = user_detect
            row.id_type_defect = id_type_defect
            row.user_assign = user_assign
        else:
            row = TicketLibrary(id_ticket=id_ticket, id_environment=id_environment, description=description,
                                creation_date=date_current, id_requirement=id_requirement, id_release=id_release,
                                user_detect=user_detect, id_type_defect=id_type_defect, user_assign=user_assign)
            self._session.add(row)

    def get_id_environment(self, id_ticket):
        TicketLibrary = self._Base.classes.ticket_library
        rows = self._session.query(TicketLibrary).filter(TicketLibrary.id_ticket == id_ticket).all()
        if len(rows) > 0:
            row = rows[0]
            return row.id_environment
        return None

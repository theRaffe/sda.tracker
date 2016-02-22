import time
from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'


class TicketBoardDao(SdaBaseDao):
    def get_ticket(self, id_ticket):
        Base = self._Base
        TicketBoard = Base.classes.ticket_board
        return self._session.query(TicketBoard).filter(TicketBoard.id_ticket == id_ticket).one()

    def get_ticket_code(self, id_ticket):
        Base = self._Base
        TicketBoard = Base.classes.ticket_board
        CatEnvironment = Base.classes.cat_environment
        CatStatusTicket = Base.classes.cat_status_ticket
        return self._session.query(TicketBoard, CatEnvironment, CatStatusTicket).join(CatEnvironment).join(
            CatStatusTicket).filter(
            TicketBoard.id_ticket == id_ticket).one()

    def add(self, dict_ticket_board):
        Base = self._Base
        TicketBoard = Base.classes.ticket_board
        date_requested = time.time()
        id_ticket = dict_ticket_board["id_ticket"]
        id_environment = dict_ticket_board["id_environment"]
        user_request = dict_ticket_board["user_request"]
        ticket_board = TicketBoard(id_ticket=id_ticket, id_environment=id_environment, id_status=1, user_request=user_request,
                         date_requested=date_requested)
        self._session.add(ticket_board)

    #def update(self, dict_ticket_board):


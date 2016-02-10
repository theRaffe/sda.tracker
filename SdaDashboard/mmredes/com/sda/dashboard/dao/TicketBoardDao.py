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

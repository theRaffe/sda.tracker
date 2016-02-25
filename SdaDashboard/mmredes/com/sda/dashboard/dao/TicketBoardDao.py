import logging
import time
from sqlalchemy.orm.exc import NoResultFound
from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'
logger = logging.getLogger(__name__)

class TicketBoardDao(SdaBaseDao):
    def get_ticket(self, id_ticket, id_status=1):
        try:
            Base = self._Base
            TicketBoard = Base.classes.ticket_board
            return self._session.query(TicketBoard).filter(
                TicketBoard.id_ticket == id_ticket and TicketBoard.id_status == id_status).one()
        except NoResultFound as e:
            logger.warning(e.message)
            return None

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
        ticket_board = TicketBoard(id_ticket=id_ticket, id_environment=id_environment, id_status=1,
                                   user_request=user_request,
                                   date_requested=date_requested)
        self._session.add(ticket_board)

    def update(self, dict_ticket_board, row=None):
        date_requested = time.time()
        user_request = dict_ticket_board["user_request"]
        id_card_ticket = dict_ticket_board["id_card_tracker"]
        id_ticket = dict_ticket_board["id_ticket"]
        id_environment = dict_ticket_board["id_environment"]

        if not row:
            Base = self._Base
            TicketBoard = Base.classes.ticket_board
            row = self._session.query(TicketBoard).filter(
                TicketBoard.id_ticket == id_ticket and TicketBoard.id_environment == id_environment).one()

        row.date_requested = date_requested
        row.user_request = user_request
        row.id_card_ticket = id_card_ticket

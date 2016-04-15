import logging
import time
from sqlalchemy.orm.exc import NoResultFound
from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'
logger = logging.getLogger(__name__)

STATUS_INSTALLED_TEST = 2
STATUS_INSTALLED_PROD = 3


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
                    TicketBoard.id_ticket == id_ticket, TicketBoard.id_environment == id_environment).one()

        row.date_requested = date_requested
        row.user_request = user_request
        row.id_card_ticket = id_card_ticket

    def update_environment(self, id_ticket, id_environment):
        base = self._Base
        TicketBoard = base.classes.ticket_board
        rows = self._session.query(TicketBoard).filter(TicketBoard.id_ticket == id_ticket).all()

        if len(rows) > 0:
            row = rows[0]
            row.id_environment = id_environment

    def update_status(self, dict_status_ticket):
        date_installed = time.time()
        id_ticket = dict_status_ticket['id_ticket']
        id_status = dict_status_ticket['id_status']
        user_installer = dict_status_ticket['user_installer']
        base = self._Base
        TicketBoard = base.classes.ticket_board
        rows = self._session.query(TicketBoard).filter(TicketBoard.id_ticket == id_ticket).all()

        if len(rows):
            row = rows[0]
            row.id_status = id_status
            row.date_installed = date_installed if id_status == STATUS_INSTALLED_TEST or id_status == STATUS_INSTALLED_PROD else row.date_installed
            row.user_installer = user_installer if id_status == STATUS_INSTALLED_TEST or id_status == STATUS_INSTALLED_PROD else row.user_installer
            return row
        return None

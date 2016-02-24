import ConfigParser
from mmredes.com.sda.dashboard.dao.CatArtifactDao import CatArtifactDao
from mmredes.com.sda.dashboard.dao.ControllerDao import ControllerDao
from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao
import unittest
import logging
from mmredes.com.sda.dashboard.dao.TicketBoardDao import TicketBoardDao

__author__ = 'macbook'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DriverTestDao(unittest.TestCase):

    def test_01(self):
        config_file = '../board.cfg'
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        controller_dao = ControllerDao(connection_file)

        cat_artifact_dao = CatArtifactDao(controller_dao.get_dict_database())

        res = cat_artifact_dao.list_all()

        m_dict = {}
        for row in res:
            m_dict[row.path_directory] = row.code_artifact

        print m_dict
        self.assertTrue(len(res) > 0)

    def test_02(self):
        config_file = '../board.cfg'
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        controller_dao = ControllerDao(connection_file)

        ticket_board_dao = TicketBoardDao(controller_dao.get_dict_database())

        m_result = ticket_board_dao.get_ticket_code('feature2')
        print m_result.ticket_board.id_ticket, m_result.cat_environment.code_environment

        self.assertTrue(m_result is not None)

    def test_03(self):
        config_file = '../board.cfg'
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        controller_dao = ControllerDao(connection_file)

        ticket_board_dao = TicketBoardDao(controller_dao.get_dict_database())

        m_result = ticket_board_dao.get_ticket('feature2')
        print m_result.__dict__

        self.assertTrue(m_result is not None)

    def test_04(self):
        config_file = '../board.cfg'
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        controller_dao = ControllerDao(connection_file)
        try:
            ticket_board_dao = TicketBoardDao(controller_dao.get_dict_database())

            dict_ticket_board = {"id_ticket" : "feature3", "id_environment" : "1", "user_request" : "rafe@mail.com"}

            ticket_board_dao.add(dict_ticket_board)

            controller_dao._session.commit()
            self.assertTrue(True)
        except RuntimeError as e:
            self.assertTrue(False, e.message)

# if __name__ == '__main__':
#     print "start test dao"
#     config_file = '../board.cfg'
#     config = ConfigParser.RawConfigParser()
#     config.read(config_file)
#     print ("sections", config.sections())
#     connection_file = config.get('DatabaseSection', 'database.file')
#     driverDao = SdaTrackerDao(connection_file)
#     row = driverDao.get_ticket_board_code("feature2")
#     print row
#
#     rows = driverDao.get_artifact_code("feature2")
#     print rows

import ConfigParser
from mmredes.com.sda.dashboard.dao.CatArtifactDao import CatArtifactDao
from mmredes.com.sda.dashboard.dao.ControllerDao import ControllerDao
from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao
import unittest
import logging
from mmredes.com.sda.dashboard.dao.TicketArtifactDao import TicketArtifactDao
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

    def test_05(self):
        config_file = '../board.cfg'
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        controller_dao = ControllerDao(connection_file)

        ticket_artifact_dao = TicketArtifactDao(controller_dao.get_dict_database())
        rows = ticket_artifact_dao.get_ticket_artifact_code('feature2')
        for row in rows:
            print row.ticket_artifact.id_ticket

        self.assertIsNotNone(rows)

    def test_06(self):
        config_file = '../board.cfg'
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        controller_dao = ControllerDao(connection_file)

        ticket_artifact_dao = TicketArtifactDao(controller_dao.get_dict_database())
        rows = ticket_artifact_dao.get_ticket_artifact_code('noticket')
        print rows
        self.assertFalse(rows)

    def test_07(self):
        config_file = '../board.cfg'
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        controller_dao = ControllerDao(connection_file)
        try:
            ticket_board_dao = TicketBoardDao(controller_dao.get_dict_database())
            row = ticket_board_dao.get_ticket('feature2')
            row.user_request = 'rafe@gmail.com'

            controller_dao._session.commit()
            self.assertTrue(True)
        except RuntimeError as e:
            self.assertTrue(False, e.message)

    def test_08(self):
        config_file = '../board.cfg'
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        connection_file = config.get('DatabaseSection', 'database.file')
        controller_dao = ControllerDao(db_path = connection_file)

        ticket_artifact_dao = TicketArtifactDao(controller_dao.get_dict_database())

        ticket_artifact = {'build_hotfix': 0, 'id_revision': 9, 'modification_user': 'rafe2004@gmail.com', 'id_type_tech': 1, 'artifacts': ['cartridge-2'], 'id_ticket': 'feature1', 'build_release': 2}
        rows = ticket_artifact_dao.process_ticket_artifact(12, ticket_artifact)

        self.assertTrue(True)
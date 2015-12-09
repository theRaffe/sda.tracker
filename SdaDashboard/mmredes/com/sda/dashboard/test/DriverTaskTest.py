import unittest

from requests import ConnectionError

from mmredes.com.sda.dashboard.management.TaskManager import TaskManager

__author__ = 'macbook'


class DriverTaskTest(unittest.TestCase):
    def test01(self):
        connected = False
        try:
            task_manager = TaskManager('../board.cfg')
            connected = True
        except ConnectionError, e:
            print "Error at connecting trello: %s" % e.message

        self.assertTrue(connected, msg="Error at connecting trello API")

        dict_board_code = {"id_ticket": "T101", "code_environment": "maab.qas",
                           "id_list_tracker": "5652a9b65a11441da81b763f", "code_status": "requested",
                           "id_card_tracker": "565e80108c046399ecc709a3"}
        list_artifact = []
        list_artifact.append({"artifact": "cartridge-1", "tech": "java", "user": "rafe@mail.com"})
        list_artifact.append({"artifact": "cartridge-2", "tech": "java", "user": "rafe@mail.com"})
        dict_board_ticket = {"dict_board": dict_board_code, "artifacts": list_artifact}

        m_card = task_manager.send_ticket_card(dict_board_ticket)
        self.assertIsNotNone(m_card, msg="card not generated")

if __name__ == '__main__':
    unittest.main()

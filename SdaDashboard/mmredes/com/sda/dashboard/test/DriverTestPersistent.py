import unittest
from mmredes.com.sda.dashboard.PersistentController import PersistentController

__author__ = 'macbook'

class DriverTestPersistent(unittest.TestCase):

    def test_01(self):
        driver = PersistentController("../board.cfg")
        row = driver.get_ticket_board('feature2')
        print row.id_ticket
        self.assertIsNotNone(row, 'error ticket does not exist')

    def test_02(self):
        driver = PersistentController("../board.cfg")
        row = driver.get_ticket_board('noticket')
        print row
        self.assertFalse(row, 'test fail')

    def test_03(self):
        driver = PersistentController("../board.cfg")
        dict = driver.get_dict_board_code('feature2')
        print dict
        self.assertIsNotNone(dict, 'error getting board code')

    def test_04(self):
        driver = PersistentController("../board.cfg")
        dict_branch = {"feature2": [{"id_artifact": 1, "email": "developer.one@gmail.com", "id_type_tech": 1}]}
        dict_result = driver.process_ticket_db(dict_branch, 2)

        self.assertEqual(dict_result["result"], "OK")

if __name__ == '__main__':
    driver = PersistentController("../board.cfg")
    print driver.get_list_artifacts()

    dict_branch = {"feature2": [{"id_artifact": 1, "email": "developer.one@gmail.com", "id_type_tech": 1}]}
    dict_result = driver.process_ticket_db(dict_branch, 2)
    print "process_ticket_db...OK"
    print ("dic_result", dict_result)



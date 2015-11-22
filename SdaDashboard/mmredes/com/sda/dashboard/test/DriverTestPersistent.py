from mmredes.com.sda.dashboard.PersistentController import PersistentController

__author__ = 'macbook'

if __name__ == '__main__':
    driver = PersistentController("../board.cfg")
    print driver.get_list_artifacts()

    dict_branch = {"feature2": [{"id_artifact": 1, "email": "developer.one@gmail.com", "id_type_tech": 1}]}
    dict_result = driver.process_ticket_db(dict_branch, 2)
    print "process_ticket_db...OK"
    print ("dic_result", dict_result)



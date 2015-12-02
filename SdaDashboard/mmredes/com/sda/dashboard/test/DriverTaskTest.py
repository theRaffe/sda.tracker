from mmredes.com.sda.dashboard.management.TaskManager import TaskManager

__author__ = 'macbook'
if __name__ == '__main__':
    task_manager = TaskManager('../board.cfg')
    print task_manager._dict_label

    dict_board_code = {"id_ticket": "T101", "code_environment": "maab.qas",
                       "id_list_tracker": "5652a9b65a11441da81b763f", "code_status": "requested", "id_card_tracker": ""}
    list_artifact = []
    list_artifact.append({"artifact": "cartridge-1", "tech": "java", "user": "rafe@mail.com"})
    list_artifact.append({"artifact": "cartridge-2", "tech": "java", "user": "rafe@mail.com"})
    dict_board_ticket = {"dict_board": dict_board_code, "artifacts": list_artifact}

    task_manager.send_ticket_card(dict_board_ticket)
    print "OK"

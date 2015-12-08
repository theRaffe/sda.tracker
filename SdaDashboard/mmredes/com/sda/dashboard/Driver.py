import os

from mmredes.com.sda.dashboard.PersistentController import PersistentController
from mmredes.com.sda.dashboard.management.TaskManager import TaskManager
from mmredes.com.sda.dashboard.repository.RepositoryListener import RepositoryListener
from mmredes.com.sda.emailing.EmailTracker import EmailTracker

cwd = os.getcwd()
config_file = os.path.join(cwd, "board.cfg")

__author__ = 'macbook'
if __name__ == '__main__':
    # x = 1
    # while True:
    #     try:
    #         print x
    #         time.sleep(1)
    #         x += 1
    #     except KeyboardInterrupt:
    #         print "Quit! See you"
    #         sys.exit()

    repository_listener = RepositoryListener(config_file)
    task_manager = TaskManager(config_file)
    is_branch_behind = repository_listener.is_behind()
    print("is behind ", is_branch_behind)
    if is_branch_behind:
        dict_branch, id_branch = repository_listener.get_branch_ticket()
        persistent_controller = PersistentController(config_file)
        print ("dict_branch", dict_branch)
        dict_board_result = persistent_controller.process_ticket_db(dict_branch, id_branch)

        if dict_board_result['result'] == 'OK':
            list_board_ticket = dict_board_result['board_ticket']
            email_tracker = EmailTracker(config_file)
            # get each ticket at board
            for board_ticket in list_board_ticket:

                dict_result = task_manager.send_ticket_card(board_ticket)
                if dict_result["result"] == "OK":
                    dict_board = board_ticket['dict_board']
                    m_card = dict_result['result_card']
                    dict_board['id_card_tracker'] = m_card.id
                    persistent_controller.update_ticket_db(dict_board)

                    dict_board_code = board_ticket['dict_board']
                    print("board_ticket", board_ticket)
                    message_email = email_tracker.get_email_ticket_request(board_ticket)
                    print("sending email...")
                    email_tracker.sendEmail(message_email)
                else:
                    print ("error send to trello", dict_result["description"])

            result_pull = repository_listener.update_local_repository()
            print(result_pull)

import logging
import os
import sys
import time

from mmredes.com.sda.dashboard.PersistentController import PersistentController
from mmredes.com.sda.dashboard.management.TaskManager import TaskManager
from mmredes.com.sda.dashboard.repository.RepositoryListener import RepositoryListener
from mmredes.com.sda.emailing.EmailTracker import EmailTracker

cwd = os.getcwd()
config_file = os.path.join(cwd, "board.cfg")
logger = logging.getLogger(__name__)
__author__ = 'macbook'


def monitor_repository():
    connected_trello = False
    task_manager = None
    if TaskManager.validate_connection():
        task_manager = TaskManager(config_file)
        connected_trello = True

    repository_listener = RepositoryListener(config_file)
    is_branch_behind = repository_listener.is_behind()
    branch_repository = repository_listener.get_current_branch()
    logger.info("is behind: %s ", is_branch_behind)

    if is_branch_behind:
        persistent_controller = PersistentController(config_file)
        dict_branch, id_branch = repository_listener.get_branch_ticket(branch_repository, persistent_controller)

        logger.info("after get_branch_ticket, dict_branch: %s" % dict_branch)
        dict_board_result = persistent_controller.process_ticket_db(dict_branch, id_branch)

        if dict_board_result['result'] == 'OK':
            list_board_ticket = dict_board_result['board_ticket']
            email_tracker = EmailTracker(config_file)
            # get each ticket at board
            for board_ticket in list_board_ticket:

                if connected_trello:
                    dict_result = task_manager.send_ticket_card(board_ticket)
                    if dict_result["result"] == "OK":
                        dict_board = board_ticket['dict_board']
                        m_card = dict_result['result_card']
                        dict_board['id_card_tracker'] = m_card.id
                        persistent_controller.update_ticket_db(dict_board)
                    else:
                        logger.error("error send to trello: %s", dict_result["description"])

                # dict_board_code = board_ticket['dict_board']
                logger.info("board_ticket: %s" % board_ticket)
                message_email = email_tracker.get_email_ticket_request(board_ticket)
                logger.info("sending email...")
                email_tracker.send_email(message_email)

            #result_pull = repository_listener.update_local_repository()
        else:
            logger.error("error at process_ticket_db: %s" % dict_board_result["description"])
        persistent_controller.close_session()


if __name__ == '__main__':
    while True:
        try:
            monitor_repository()
            time.sleep(60)
        except KeyboardInterrupt:
            print("Quit! See you")
            sys.exit()

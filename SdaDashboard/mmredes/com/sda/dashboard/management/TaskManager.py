import ConfigParser
from trello import TrelloClient
from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao

__author__ = 'macbook'

class TaskManager():
    client_trello = None
    o_board = None
    config_file = ''

    def __init__(self, config_file):
        self.config_file = config_file
        config = ConfigParser.RawConfigParser()
        config.read(config_file)

        api_key = config.get('Management.Task', 'api.key')
        oath_token = config.get('Management.Task', 'oath.token')
        id_board = config.get('Management.Task', 'id.board')
        self.client_trello = TrelloClient(api_key,token=oath_token)
        o_board = self.client_trello.get_board(self.id_board)

    def refresh_list_id(self):
        dao_object = SdaTrackerDao(self.config_file)
        for a_list in self.o_board.all_lists():
            code_env = a_list.name
            id_list_tracker = a_list.id
            dao_object.update_list_tracker(code_env, id_list_tracker)

    def get_card_ticket(self, dict_board_ticket):
        dict_board = dict_board_ticket['dict_board']
        id_ticket = dict_board['id_ticket']
        id_list_tracker = dict_board['id_list_tracker']
        a_list = self.o_board.get_list(id_list_tracker)
        for a_card in a_list.list_cards():
            if a_card.name == id_ticket:
                return a_card
        return None

    def send_ticket_card(self, dict_board_ticket):
        a_card = self.get_card_ticket(dict_board_ticket)
        if a_card:
            print "update card"
        else:
            print "new card"

        return None

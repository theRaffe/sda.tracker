import json
import ConfigParser
from trello import TrelloClient
from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao

__author__ = 'macbook'

class TaskManager():
    client_trello = None
    _board = None
    _board_labels = None
    config_file = ''

    def __init__(self, config_file):
        self.config_file = config_file
        config = ConfigParser.RawConfigParser()
        config.read(config_file)

        api_key = config.get('Management.Task', 'api.key')
        oath_token = config.get('Management.Task', 'oath.token')
        id_board = config.get('Management.Task', 'id.board')
        self.client_trello = TrelloClient(api_key,token=oath_token)
        self._board = self.client_trello.get_board(self.id_board)
        self._board_labels = self._board.get_labels()

    def refresh_list_id(self):
        dao_object = SdaTrackerDao(self.config_file)
        for a_list in self.o_board.all_lists():
            code_env = a_list.name
            id_list_tracker = a_list.id
            dao_object.update_list_tracker(code_env, id_list_tracker)

    def get_card_ticket(self, id_card_tracker):
        return self.client_trello.get_card(id_card_tracker)

    def send_ticket_card(self, dict_board_ticket):
        dict_board = dict_board_ticket['dict_board']
        id_card_tracker = dict_board['id_card_tracker']
        a_card = self.get_card_ticket(id_card_tracker)

        if a_card:
            print "update card"
        else:
            print "new card"
            list_artifact = dict_board_ticket['artifacts']
            id_list_tracker = dict_board['id_list_tracker']
            id_ticket = dict_board['id_ticket']
            string_json = json.dumps(list_artifact, indent=2)
            a_list = self._board.get_list(id_list_tracker)
            labels_artifact = self.get_labels_artifact(list_artifact)

            new_card = a_list.add(id_ticket, string_json)
            for label in labels_artifact:
                new_card.add_label(label)


        return None

    def get_labels_artifact(self, list_artifact):
        list_label = []
        for dict_artifact in list_artifact:
            artifact = dict_artifact['artifact']
            ls = [label for label in self._board_labels if label.name == artifact]
            if len(ls) == 0:
                label = self._board.add_label(artifact, None)
                self._board_labels = self._board.get_labels()
                list_label.append(label)
            else:
                list_label.append(ls[0])
        return list_label

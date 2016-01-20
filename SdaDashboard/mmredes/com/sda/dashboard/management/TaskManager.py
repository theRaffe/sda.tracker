import json
import ConfigParser
import logging

import requests
from requests.exceptions import ReadTimeout
from requests.packages.urllib3.exceptions import ConnectionError
from trello import TrelloClient

from mmredes.com.sda.dashboard.dao.SdaTrackerDao import SdaTrackerDao

__author__ = 'macbook'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class TaskManager():
    _client_trello = None
    _board = None
    _board_labels = None
    _config_file = ''
    _dict_label = {}

    def __init__(self, config_file):
        self._config_file = config_file
        config = ConfigParser.RawConfigParser()
        config.read(config_file)

        api_key = config.get('Management.Task', 'api.key')
        oath_token = config.get('Management.Task', 'oath.token')
        id_board = config.get('Management.Task', 'id.board')
        self._client_trello = TrelloClient(api_key, token=oath_token)
        self._board = self._client_trello.get_board(id_board)
        self._board_labels = self._board.get_labels()
        list_label = [label for label in self._board_labels if label.name != '' and label.color]
        for label in list_label:
            self._dict_label[label.name] = label

    @staticmethod
    def validate_connection():
        url_test = 'https://api.trello.com/1'
        try:
            result = requests.request('GET', url_test, timeout=5)
            return result.status_code == 200
        except ConnectionError as e:
            logger.warning("couldn't connect to trello, see error: %s" % e.message)
            return False
        except ReadTimeout as e:
            logger.warning("couldn't connect to trello, timeout error: %s" % e.message)
            return False

    def refresh_list_id(self):
        dao_object = SdaTrackerDao(self._config_file)
        for a_list in self._board.all_lists():
            code_env = a_list.name
            id_list_tracker = a_list.id
            dao_object.update_list_tracker(code_env, id_list_tracker)

    def get_card_ticket(self, id_card_tracker):
        return self._client_trello.get_card(id_card_tracker) if id_card_tracker else None

    def send_ticket_card(self, dict_board_ticket):
        """Send new card or update it"""
        result_card = None
        dict_board = dict_board_ticket['dict_board']
        id_card_tracker = dict_board['id_card_tracker']
        try:
            action = None
            # get trello's card
            a_card = self.get_card_ticket(id_card_tracker)
            list_artifact = dict_board_ticket['artifacts']
            # get id_list trello
            id_list_tracker = dict_board['id_list_tracker']
            # id_ticket = card.name
            id_ticket = dict_board['id_ticket']
            # card's description
            string_json = json.dumps(list_artifact, indent=2)
            labels_artifact = self.get_labels_artifact(list_artifact)

            if a_card:
                action = "UPDATE"
                #print "update card"
                for label in a_card.labels:
                    a_card.client.fetch_json(
                        '/cards/' + a_card.id + '/idLabels/' + label.id,
                        http_method='DELETE')

                a_card.set_description(string_json)
                result_card = a_card

            else:
                action = "NEW"
                #print "new card"
                a_list = self._board.get_list(id_list_tracker)
                new_card = a_list.add_card(id_ticket, string_json)
                result_card = new_card

            result_card.add_label(self._dict_label['requested'])
            for label in labels_artifact:
                result_card.add_label(label)
            return {"result": "OK", "action": action, "result_card": result_card}
        except RuntimeError as e:
            return {"result": "ERROR", "description": e.message}

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




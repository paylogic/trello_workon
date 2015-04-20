"""Models for a Trello Board."""
import requests

from models.list import List

TRELLO_BOARD_REQUEST = 'https://api.trello.com/1/board/{board_id}?key={app_id}&token={token}'
TRELLO_LISTS_REQUEST = 'https://api.trello.com/1/boards/{board_id}/lists?key={app_id}&token={token}'


class Board(object):
    """Represents a Trello board."""

    def __init__(self, board_id, trello_settings):
        self.board_id = board_id
        self.trello_settings = trello_settings

        self.name = requests.get(
            TRELLO_BOARD_REQUEST.format(
                board_id=self.board_id,
                app_id=self.trello_settings['app_id'],
                token=self.trello_settings['token'],
            )
        ).json()['name']
        self.load_list_ids()

        self.todo = List(self, 'To Do')
        self.doing = List(self, 'Doing')
        self.done = List(self, 'Done')
        self.fires = List(self, 'Fires')
        self.us_todo = List(self, 'User Stories')
        self.us_done = List(self, 'User Stories - Done in sprint')

    def get_current_workon(self):
        doing = self.doing.get_top_card_for_users()
        doing.update(self.fires.get_top_card_for_users())
        return doing

    def load_list_ids(self):
        response = requests.get(
            TRELLO_LISTS_REQUEST.format(
                board_id=self.board_id,
                app_id=self.trello_settings['app_id'],
                token=self.trello_settings['token'],
            )
        ).json()

        self.list_ids = {}
        for trello_list in response:
            self.list_ids[trello_list['name']] = trello_list['id']

    def get_list_id(self, list_name):
        if not hasattr(self, 'list_ids'):
            self.load_list_ids()
        return self.list_ids[list_name]

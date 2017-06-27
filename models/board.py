"""Models for a Trello Board."""
import requests

from models.user import TrelloTokenError
from models.list import List
from settings import DOING_LIST_ID

TRELLO_BOARD_REQUEST = 'https://api.trello.com/1/board/{board_id}?key={app_id}&token={token}'
TRELLO_LISTS_REQUEST = 'https://api.trello.com/1/boards/{board_id}/lists?key={app_id}&token={token}'


class Board(object):
    """Represents a Trello board."""

    def __init__(self, board_id, trello_settings):
        self.board_id = board_id
        self.trello_settings = trello_settings

        try:
            self.name = requests.get(
                TRELLO_BOARD_REQUEST.format(
                    board_id=self.board_id,
                    app_id=self.trello_settings['app_id'],
                    token=self.trello_settings['token'],
                )
            ).json()['name']
        except ValueError:
            raise TrelloTokenError

        self.load_list_names()
        self.doing = List(self, DOING_LIST_ID)

    def get_current_workon(self):
        doing = self.doing.get_top_card_for_users()
        return doing

    def load_list_names(self):
        try:
            response = requests.get(
                TRELLO_LISTS_REQUEST.format(
                    board_id=self.board_id,
                    app_id=self.trello_settings['app_id'],
                    token=self.trello_settings['token'],
                )
            ).json()
        except ValueError:
            raise TrelloTokenError

        self.list_names = {}
        for trello_list in response:
            self.list_names[trello_list['id']] = trello_list['name']

    def get_list_name(self, list_id):
        """Get list name based on list id."""
        if not hasattr(self, 'list_names'):
            self.load_list_names()
        return self.list_names[list_id]

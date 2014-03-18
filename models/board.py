"""Models for a Trello Board."""
import requests

from models import Card

TRELLO_LISTS_REQUEST = 'https://trello.com/1/boards/{board_id}/lists?key={app_id}&token={token}'



def from_board_id(board_id):
    """Create a Board object from a trello board id"""

class Board(object):
    """Represents a Trello board."""
    users = []
    board_id = None
    _doing_list_id = None
    doing_cards = None
    _fires_list_id = None
    fires_cards = None

    def __init__(self, board_id):
        self.board_id = board_id
        self.load_doing()
        self.load_fires()

    def add_user(self, user):
        self.users.append(user)
        user.board_id = self.board_id

    def remove_user(self, user):
        self.users.remove(user)
        user.board_id = None

    def load_doing(self):
        self._doing_list_id = tr.get_list_id_from_board_by_name(self.board_id, "Doing")
        self.doing_cards = Card.from_list_id(self._doing_list_id)

    def load_fires(self):
        self._fires_list_id = tr.get_list_id_from_board_by_name(self.board_id, "Fires")
        self.fire_cards = Card.from_list_id(self._fires_list_id)

    def get_list_by_name(self, name):
        response = requests.get(
            TRELLO_LISTS_REQUEST.format(
                board_id=board_id,
                app_id=TRELLO_APP_KEY,
                token=TRELLO_TOKEN,
            )
        )
        for trello_list in response.json():
            if trello_list['name'] == name:
                return trello_list['id']



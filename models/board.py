"""Models for a Trello Board."""
import requests

from models.list import List

TRELLO_BOARD_REQUEST = 'https://api.trello.com/1/board/{board_id}?key={app_id}&token={token}'


def from_board_id(board_id):
    """Create a Board object from a trello board id"""


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

        self.todo = List(self, 'To Do')
        self.doing = List(self, 'Doing')
        self.done = List(self, 'Done')
        self.fires = List(self, 'Fires')

    def get_current_workon(self):
        doing = self.doing.get_top_card_for_users()
        doing.update(self.fires.get_top_card_for_users())
        return doing

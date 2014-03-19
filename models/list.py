"""Models for a Trello list."""
import requests

from models.card import from_list_id

TRELLO_LISTS_REQUEST = 'https://trello.com/1/boards/{board_id}/lists?key={app_id}&token={token}'


class List(object):
    """Representation of a Trello list."""

    def __init__(self, board, name):
        self.board = board
        self.name = name
        self.cards = self.load_cards()

    def load_cards(self):
        list_id = self.get_list_id()
        return from_list_id(list_id)

    def get_list_id(self):
        if not hasattr(self.board, 'lists_request_json'):
            self.board.lists_requests_response = requests.get(
                TRELLO_LISTS_REQUEST.format(
                    board_id=self.board.board_id,
                    app_id=self.board.trello_settings['app_id'],
                    token=self.board.trello_settings['token'],
                )
            ).json()

        for trello_list in self.board.lists_requests_response:
            if trello_list['name'] == self.name:
                return trello_list['id']

    def get_top_card_for_users(self):
        users = {}
        for card in self.cards:
            for user in card.assigned_to:
                users.setdefault(user, card)

        return users

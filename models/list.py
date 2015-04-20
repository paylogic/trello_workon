"""Models for a Trello list."""

from models.card import from_list


class List(object):
    """Representation of a Trello list."""

    def __init__(self, board, name):
        self.board = board
        self.name = name
        self.list_id = board.get_list_id(name)
        self.cards = self.load_cards()

    def load_cards(self):
        return from_list(self)

    def get_top_card_for_users(self):
        users = {}
        for card in self.cards:
            for user in card.assigned_to:
                users.setdefault(user, card)

        return users

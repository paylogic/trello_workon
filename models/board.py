"""Models for a Trello Board."""
import util.trello_requests as tr


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
        doing_cards = tr.get_cards_from_list(self._doing_list_id)

    def load_fires(self):
        self._fires_list_id = tr.get_list_id_from_board_by_name(self.board_id, "Fires")
        self.fire_cards = tr.get_cards_from_list(self._fires_list_id)

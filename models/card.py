"""Classes and functions for a Trello card."""
import requests
from settings import TRELLO_APP_KEY, TRELLO_TOKEN

TRELLO_LIST_CARD_REQUEST = 'https://trello.com/1/lists/{list_id}/cards?key={app_id}&token={token}'


def from_list_id(list_id):
    """Create Card objects for the cards in a list."""
    response = requests.get(
        TRELLO_LIST_CARD_REQUEST.format(
            list_id=list_id,
            app_id=TRELLO_APP_KEY,
            token=TRELLO_TOKEN,
        )
    )
    import pdb; pdb.set_trace()
    return response.json()


class Card(object):
    """Represents a Trello card."""
    card_id = None
    assigned_to = None

    def __init__(self, card_id, assigned_to):
        self.card_id = card_id
        self.assigned_to = assigned_to

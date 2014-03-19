"""Classes and functions for a Trello card."""
import re
import requests
from settings import TRELLO_APP_ID, TRELLO_TOKEN
from models.user import User


TRELLO_LIST_CARD_REQUEST = 'https://trello.com/1/lists/{list_id}/cards?key={app_id}&token={token}'


def from_list_id(list_id):
    """Create Card objects for the cards in a list."""
    response = requests.get(
        TRELLO_LIST_CARD_REQUEST.format(
            list_id=list_id,
            app_id=TRELLO_APP_ID,
            token=TRELLO_TOKEN,
        )
    )
    cards = []
    for entry in response.json():
        cards.append(Card(entry))
    return cards


class Card(object):
    """Represents a Trello card."""
    def __str__(self):
        return '<Card: {0}>'.format(self.name)

    def __repr__(self):
        return str(self)

    def __init__(self, card_dict):

        self.name = card_dict['name']
        try:
            match = re.match(r'([\d]+).*\(([\d+])k\)', self.name)
            self.case_number = match.group(1)
            self.task_estimate = match.group(2)
        except (IndexError, AttributeError):
            pass  # Card name doesn't match, so case number and/or task estimate are not set.

        if card_dict['idMembers'] != []:
            self.assigned_to = User.query.filter(User.trello_user_id.in_(card_dict['idMembers'])).all()
        else:
            self.assigned_to = []

"""Classes and functions for a Trello card."""
import re
import requests
from settings import TRELLO_APP_ID, TRELLO_TOKEN
from models.user import User


TRELLO_LIST_CARD_REQUEST = 'https://api.trello.com/1/lists/{list_id}/cards?key={app_id}&token={token}'


def from_list(trello_list):
    """Create Card objects for the cards in a list."""
    response = requests.get(
        TRELLO_LIST_CARD_REQUEST.format(
            list_id=trello_list.list_id,
            app_id=TRELLO_APP_ID,
            token=TRELLO_TOKEN,
        )
    ).json()
    cards = []
    for entry in response:
        cards.append(Card(trello_list, entry, trello_list.name))  # status is based on list name
    return cards


class Card(object):
    """Represents a Trello card."""

    def __str__(self):
        return '<Card: {0}, estimation: {1}>'.format(self.name, self.task_estimate or 'None')

    def __repr__(self):
        return str(self)

    def __init__(self, containing_list, card_dict, status):
        self.status = status
        self.list = containing_list
        self.name = card_dict['name']

        try:
            self.task_estimate = int(re.search(r'\((\d+)k\)', self.name).group(1))
        except (IndexError, AttributeError):
            self.task_estimate = 0  # Card name doesn't match, so task estimate was not set.

        try:
            # Match '[123] case title' OR '123 case title' saving only the case number
            self.case_number = int(re.search(r'^\[?(\d+)', self.name).group(1))
        except (IndexError, AttributeError):
            self.case_number = None  # Card name doesn't match, so case number was not set

        if card_dict['idMembers'] != []:
            self.assigned_to = User.query.filter(User.trello_user_id.in_(card_dict['idMembers'])).all()
        else:
            self.assigned_to = []

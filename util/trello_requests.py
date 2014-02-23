"""Utility functions for getting data from Trello."""

import re
import requests

from util.settings import TRELLO_APP_ID, TRELLO_TOKEN

TRELLO_BOARD_REQUEST = 'https://api.trello.com/1/board/{board_id}?key={app_id}&token={token}'
TRELLO_LISTS_REQUEST = 'https://trello.com/1/boards/{board_id}/lists?key={app_id}&token={token}'
TRELLO_LIST_CARD_REQUEST = 'https://trello.com/1/lists/{list_id}/cards?key={app_id}&token={token}'
TRELLO_MEMBER_REQUEST = 'https://trello.com/1/member/{user_id}?key={app_id}&token={token}'


def get_user_name(user_id):
    """Gets the full name of the user """
    response = requests.get(
        TRELLO_MEMBER_REQUEST.format(
            user_id=user_id,
            app_id=TRELLO_APP_ID,
            token=TRELLO_TOKEN,
        )
    )
    return response.json()['fullName']

def get_user_case_map(user_cases):
    users = []
    for user, case in user_cases.iteritems():
        match = re.match(r'^([0-9]+) - .*$', case)
        try:
            case_no = match.group(1)
            user_name = get_user_name(user)
            users.append((user_name, case_no))
        except AttributeError:  # No match
            pass
    return users


def get_top_doing_for_users(cards):
    user_cases = {}

    for card in cards:
        if card['idMembers']:
            for member in card['idMembers']:
                if not member in user_cases:
                    user_cases[member] = card['name']

    return user_cases


def get_doing_list_cards_from_board(list_id):
    response = requests.get(
        TRELLO_LIST_CARD_REQUEST.format(
            list_id=list_id,
            app_id=TRELLO_APP_ID,
            token=TRELLO_TOKEN,
        )
    )
    return response.json()


def get_doing_list_id_from_board(board_id):
    response = requests.get(
        TRELLO_LISTS_REQUEST.format(
            board_id=board_id,
            app_id=TRELLO_APP_ID,
            token=TRELLO_TOKEN,
        )
    )
    for trello_list in response.json():
        if trello_list['name'] == 'Doing':
            return trello_list['id']

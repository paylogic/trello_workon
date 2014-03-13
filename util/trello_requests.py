"""Utility functions for getting data from Trello."""
from settings import TRELLO_TOKEN

import re
import requests

TRELLO_BOARD_REQUEST = 'https://api.trello.com/1/board/{board_id}?key={app_id}&token={token}'
TRELLO_LISTS_REQUEST = 'https://trello.com/1/boards/{board_id}/lists?key={app_id}&token={token}'
TRELLO_LIST_CARD_REQUEST = 'https://trello.com/1/lists/{list_id}/cards?key={app_id}&token={token}'
TRELLO_MEMBER_REQUEST = 'https://trello.com/1/member/{user_id}?key={app_id}&token={token}'
TRELLO_MY_USER = 'https://trello.com/1/member/my?key={app_id}&token={token}'

TRELLO_APP_KEY = '7eab1e3ace4171b6a45321352035e504'


def get_token_user_id(token):
    response = requests.get(
        TRELLO_MY_USER.format(
            app_id=TRELLO_APP_KEY,
            token=token,
        )
    )
    return response.json()['id']

def get_user_case_number(user_cases):
    users = {}
    for user, case in user_cases.iteritems():
        match = re.match(r'^([0-9]+) - .*$', case)
        try:
            case_no = match.group(1)
            users[user] = case_no
        except AttributeError:  # No match
            pass
    return users


def get_top_card_for_users(cards):
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
            app_id=TRELLO_APP_KEY,
            token=TRELLO_TOKEN,
        )
    )
    return response.json()


def get_list_id_from_board_by_name(board_id, name):
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

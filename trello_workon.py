import sys

import requests

from models.board import Board
from models.user import User
from models.case import create_cases_from_board
from models.base import db_session

from settings import TRELLO_TOKEN, TRELLO_APP_ID

DEBUG = True


def dbg_print(msg):
    if DEBUG:
        print(msg)

if __name__ == '__main__':
    if '--silent' in sys.argv:
        DEBUG = False

    dbg_print('running trello_workon')

    trello_settings = {
        'app_id': TRELLO_APP_ID,
        'token': TRELLO_TOKEN,
    }

    dbg_print('getting board ids (comm. with burndown)')
    board_ids = requests.get('http://10.0.31.52/dashboard/?format=json').json()

    dbg_print('creating boards (comm. with Trello)')
    boards = [Board(board_id, trello_settings) for board_id in board_ids]

    dbg_print('applying logic.')
    cases = {}
    working_on = {}
    for board in boards:
        working_on.update(board.get_current_workon())
        for case in create_cases_from_board(board):
            cases[case.case_number] = case

    users = User.query.all()
    for user in users:
        card = working_on.get(user)
        try:
            dbg_print(user.workon(card))
        except Exception as e:
            print "error in workon for user {0}: {1}".format(user.username, user.fogbugz_token)
            print repr(e)
        if card:
            user.board_id = card.list.board.board_id
            db_session.commit()

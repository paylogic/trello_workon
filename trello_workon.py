from raven import Client

client = Client('https://52c762c180664061ac51abcb12f5b86e:04f8f41e2166443da6c3ab6ca50127cf@sentry-dev.paylogic.eu/37')

import sys

from models.board import Board
from models.user import User
from models.case import create_cases_from_board
from models.base import db_session

from settings import TRELLO_TOKEN, TRELLO_APP_ID, BOARD_ID

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

    dbg_print('creating boards (comm. with Trello)')

    # In kanban there is only 1 board
    board = Board(BOARD_ID, trello_settings)

    dbg_print('applying logic.')
    cases = {}
    working_on = {}
    working_on.update(board.get_current_workon())
    for case in create_cases_from_board(board):
        cases[case.case_number] = case

    users = User.query.all()
    for user in users:
        card = working_on.get(user)
        try:
            dbg_print(user.workon(card))
        except Exception as e:
            client.captureException()
        if card:
            user.board_id = card.list.board.board_id
            db_session.commit()

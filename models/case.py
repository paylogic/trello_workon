from itertools import groupby
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm.exc import NoResultFound

from models.base import Base, db_session


def create_cases_from_board(board):
    def case_number(card):
        return card.case_number

    cases = {}
    cards = board.todo.cards + board.doing.cards + board.done.cards
    cards = sorted(cards, key=case_number)
    for case_no, case_cards in groupby(cards, key=case_number):
        case = get_or_create(case_no)
        for card in list(case_cards):
            case.add(card)
        cases[case_no] = case

    user_stories = board.us_todo.cards + board.us_done.cards
    [
        cases[card.case_number].add(card)
        for card in user_stories if hasattr(card, 'case_number') and card.case_number in cases
    ]
    db_session.commit()

    return cases.values()


def get_or_create(case_number):
    if not case_number:
        case_number = 0
    try:
        case = Case.query.filter(Case.case_number == case_number).one()
        case.todo = []
        case.doing = []
        case.done = []
        return case
    except NoResultFound:
        case = Case(case_number)
        db_session.add(case)
        return case


class Case(Base):
    __tablename__ = 'trello_fogbugz_cases'
    id = Column(Integer, primary_key=True)
    case_number = Column(Integer, nullable=True, default=0)
    case_desc = Column(String(255), nullable=False, default='')
    todo_sum = Column(Integer, nullable=False, default=0)
    doing_sum = Column(Integer, nullable=False, default=0)
    done_sum = Column(Integer, nullable=False, default=0)

    def __init__(self, case_number):
        self.case_number = case_number
        self.todo = []
        self.doing = []
        self.done = []

    def add(self, card):
        if card.status == 'To Do':
            self.todo.append(card)
        elif card.status == 'Doing':
            self.doing.append(card)
        elif card.status == 'Done':
            self.done.append(card)

        self.case_desc = card.name
        self.set_progress()


    def set_progress(self):
        def estimated_sum(card_list):
            return sum([card.task_estimate for card in card_list])

        self.todo_sum = estimated_sum(self.todo)
        self.doing_sum = estimated_sum(self.doing)
        self.done_sum = estimated_sum(self.done)

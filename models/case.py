from itertools import groupby
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm.exc import NoResultFound
import re

from models.base import Base, db_session


def create_cases_from_board(board):
    def case_number(card):
        return card.case_number

    cases = {}
    cards = board.doing.cards
    cards = sorted(cards, key=case_number)
    for case_no, case_cards in groupby(cards, key=case_number):
        case = get_or_create(case_no)
        for card in list(case_cards):
            case.add(card)
        cases[case_no] = case

    db_session.commit()

    return cases.values()


def get_or_create(case_number):
    if not case_number:
        case_number = 0
    try:
        case = Case.query.filter(Case.case_number == case_number).one()
        case.doing = []
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

    def __init__(self, case_number):
        self.case_number = case_number
        self.doing = []

    def add(self, card):
        self.case_desc = ''

        if re.search(r'Doing', card.status):
            self.doing.append(card)
        else:
            self.case_desc = card.name

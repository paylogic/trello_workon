from sqlalchemy import Column, String, Integer

from models.base import Base, db_session
from models.case import get_or_create

from util.trello_requests import get_token_user_id
from util import fogbugz_requests as fr


class FogbugzTokenError(ValueError):
    """Error raised for an invalid fogbugz token."""


class TrelloTokenError(ValueError):
    """Error raised for an invalid trello token."""


class User(Base):
    __tablename__ = 'trello_fogbugz_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    trello_user_id = Column(String(30), nullable=False)
    fogbugz_token = Column(String(30), nullable=False)
    current_case = Column(Integer, nullable=True, default=None)

    # Fields to be able to show current working status on burndown
    board_id = Column(String(20), nullable=True, default=None)
    fogbugz_case = Column(String(255), nullable=False, default='')

    def __init__(self, username, trello_token, fogbugz_token):
        self.username = username
        try:
            self.trello_user_id = get_token_user_id(trello_token)
        except ValueError:
            raise TrelloTokenError
        if fr.is_correct_token(fogbugz_token):
            self.fogbugz_token = fogbugz_token
        else:
            raise FogbugzTokenError

    def __repr__(self):
        return '<{0}: {1} ({2})>'.format(self.__class__.__name__, self.id, self.username)

    def is_in_schedule_time(self):
        return fr.is_in_schedule_time(self.fogbugz_token)

    def start_work(self, card, commit_to_fogbugz=True):
        if card.case_number:
            if commit_to_fogbugz:
                fr.start_work_on(self.fogbugz_token, card.case_number)
            case = get_or_create(card.case_number)
            self.fogbugz_case = case.case_desc or card.name
            self.current_case = card.case_number
        else:
            if commit_to_fogbugz:
                fr.stop_work(self.fogbugz_token)
            self.fogbugz_case = card.name
            self.current_case = 0

        db_session.commit()

    def stop_work(self):
        fr.stop_work(self.fogbugz_token)
        self.fogbugz_case = ''
        self.current_case = 0
        db_session.commit()

    def workon(self, card):
        if not self.is_in_schedule_time():
            try:
                if self.current_case:
                    return "{0} stopped work, as it is outside working time".format(self.username)
                else:
                    return "{0} is still outside working time".format(self.username)
            finally:
                self.stop_work()

        if not card:
            try:
                if self.current_case:
                    old_case = self.current_case
                    return "{0} stopped work on {1}".format(self.username, old_case)
                else:
                    return "{0} is still not working on a case".format(self.username)
            finally:
                self.stop_work()

        if not card.case_number:
            self.start_work(card)
            return "{0} is working on a case without case number".format(self.username)

        if self.current_case != card.case_number:
            self.start_work(card)
            return "{0} started working on {1}".format(self.username, self.current_case)
        else:
            self.start_work(card, commit_to_fogbugz=False)
            return "{0} is still working on {1}".format(self.username, self.current_case)

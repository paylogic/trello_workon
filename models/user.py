from sqlalchemy import Column, String, Integer

from models.base import Base, db_session
from models.case import Case

from util.trello_requests import get_token_user_id
from util import fogbugz_requests as fr


FOGBUGZ_URL = 'https://case.paylogic.eu/fogbugz/api.asp'


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

    def is_in_schedule_time(self):
        return fr.is_in_schedule_time(self.fogbugz_token)

    def get_fogbugz_case(self):
        return fr.get_working_on(self.fogbugz_token)

    def start_work(self, card):
        if card.case_number:
            fr.start_work_on(self.fogbugz_token, card.case_number)
            self.fogbugz_case = Case.query.filter(Case.case_number == card.case_number).one().case_desc
            self.current_case = card.case_number
        else:
            self.fogbugz_case = card.name
            self.current_case = 0

        db_session.commit()

    def stop_work(self):
        if self.current_case:
            fr.stop_work(self.fogbugz_token)
        self.fogbugz_case = ''
        self.current_case = None
        db_session.commit()

    def workon(self, card):
        fb_working_on = self.get_fogbugz_case()
        manual = fb_working_on not in [0, self.current_case]
        if manual:
            self.fogbugz_case = fr.get_case_name(self.fogbugz_token, fb_working_on)
            return "{0} is currently working on a manually set case: {1}".format(self.username, fb_working_on)

        if not self.is_in_schedule_time():
            if self.current_case is not None:
                self.stop_work()
                return "{0} stopped work, as it is outside working time".format(self.username)
            else:
                return "{0} is still outside working time".format(self.username)

        if not card:
            if self.current_case is not None:
                old_case = self.current_case
                self.stop_work()
                return "{0} stopped work on {1}".format(self.username, old_case)
            else:
                return "{0} is still not working on a case".format(self.username)

        if not card.case_number:
            self.start_work(card)
            return "{0} is working on a case without case number".format(self.username)

        if self.current_case != card.case_number:
            self.start_work(card)
            return "{0} started working on {1}".format(self.username, self.current_case)
        else:
            return "{0} is still working on {1}".format(self.username, self.current_case)


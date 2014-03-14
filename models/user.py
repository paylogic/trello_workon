from sqlalchemy import Column, String, Integer

from models.base import Base

from util.trello_requests import get_token_user_id
from util.fogbugz_requests import is_correct_token


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
    current_case = Column(Integer, nullable=False, default=0)

    # Fields to be able to show current working status on burndown
    board_id = Column(String(20), nullable=True, default=None)
    fogbugz_case = Column(String(255), nullable=False, default='')

    def __init__(self, username, trello_token, fogbugz_token):
        self.username = username
        try:
            self.trello_user_id = get_token_user_id(trello_token)
        except ValueError:
            raise TrelloTokenError
        if is_correct_token(fogbugz_token):
            self.fogbugz_token = fogbugz_token
        else:
            raise FogbugzTokenError

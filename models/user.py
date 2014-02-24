from sqlalchemy import Column, String, Integer

from models.base import Base


class User(Base):
    __tablename__ = 'trello_fogbugz_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    trello_token = Column(String(64), nullable=False)
    fogbugz_token = Column(String(30), nullable=False)

    def __init__(self, username, trello_token, fogbugz_token):
        self.username = username
        self.trello_token = trello_token
        self.fogbugz_token = fogbugz_token

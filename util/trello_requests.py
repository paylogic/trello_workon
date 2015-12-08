"""Utility functions for getting data from Trello."""
from settings import TRELLO_APP_ID

import requests

TRELLO_MY_USER = 'https://trello.com/1/member/my?key={app_id}&token={token}'


def get_token_user_id(token):
    """Get the Trello user id token."""
    response = requests.get(
        TRELLO_MY_USER.format(
            app_id=TRELLO_APP_ID,
            token=token,
        )
    )
    return response.json()['id']

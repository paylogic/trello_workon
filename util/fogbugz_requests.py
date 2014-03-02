"""Utility functions for getting data from Fogbugz."""
import requests
import datetime

from bs4 import BeautifulSoup

FOGBUGZ_URL = 'https://case.paylogic.eu/fogbugz/api.asp'


def get_current_est(trello_token, case_number):
    response = requests.get(
        url=FOGBUGZ_URL,
        params={
            'token': trello_token,
            'cmd': 'search',
            'q': case_number,
            'cols': 'hrsCurrEst',
        }
    ).text
    bs = BeautifulSoup(response, 'xml')

    assert not bs.find('error')
    return bs.find('hrsCurrEst').getText()


def set_current_est(trello_token, case_number, estimate):
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': trello_token,
            'cmd': 'edit',
            'ixBug': case_number,
            'hrsCurrEst': estimate,
        }
    ).text

    assert not BeautifulSoup(response, 'xml').find('error')


def get_working_on(trello_token):
    response = requests.get(
        FOGBUGZ_URL,
        params={
            'token': trello_token,
            'cmd': 'viewPerson',
        }
    ).text
    bs = BeautifulSoup(response, 'xml')

    assert not bs.find('error')
    return int(bs.find('ixBugWorkingOn').getText())


def start_work_on(trello_token, case_number):
    if get_current_est(trello_token, case_number):
        set_current_est(trello_token, case_number, 1)
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': trello_token,
            'cmd': 'startWork',
            'ixBug': case_number,
        },
    ).text

    assert not BeautifulSoup(response, 'xml').find('error')


def stop_work_on(trello_token, case_number):
    if not get_working_on(trello_token) == int(case_number):
        return
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': trello_token,
            'cmd': 'stopWork',
        }
    ).text

    assert not BeautifulSoup(response, 'xml').find('error')

def is_in_schedule_time(trello_token):
    response = requests.get(
        url=FOGBUGZ_URL,
        params={
            'token': trello_token,
            'cmd': 'listWorkingSchedule',
        }
    )

    import pdb; pdb.set_trace()

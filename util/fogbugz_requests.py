"""Utility functions for getting data from Fogbugz."""
import requests
from datetime import datetime, timedelta

import isodate
from bs4 import BeautifulSoup

FOGBUGZ_URL = 'https://case.paylogic.eu/fogbugz/api.asp'


def is_correct_token(fogbugz_token):
    response = requests.get(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'listFilters',
        }
    ).text
    bs = BeautifulSoup(response, 'xml')

    return not bs.find('error')


def get_current_est(fogbugz_token, case_number):
    response = requests.get(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'search',
            'q': case_number,
            'cols': 'hrsCurrEst',
        }
    ).text
    bs = BeautifulSoup(response, 'xml')

    assert not bs.find('error')

    if bs.find('hrsCurrEst'):
        return bs.find('hrsCurrEst').getText()
    else:
        return None


def set_current_est(fogbugz_token, case_number, estimate):
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'edit',
            'ixBug': case_number,
            'hrsCurrEst': estimate,
        }
    ).text

    assert not BeautifulSoup(response, 'xml').find('error')


def get_working_on(fogbugz_token):
    response = requests.get(
        FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'viewPerson',
        }
    ).text
    bs = BeautifulSoup(response, 'xml')

    assert not bs.find('error')
    return int(bs.find('ixBugWorkingOn').getText())


def start_work_on(fogbugz_token, case_number):
    if get_current_est(fogbugz_token, case_number):
        set_current_est(fogbugz_token, case_number, 1)
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'startWork',
            'ixBug': case_number,
        },
    ).text

    assert not BeautifulSoup(response, 'xml').find('error')


def stop_work_on(fogbugz_token, case_number):
    if not get_working_on(fogbugz_token) == int(case_number):
        return
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'stopWork',
        }
    ).text

    assert not BeautifulSoup(response, 'xml').find('error')


def is_in_schedule_time(fogbugz_token):

    now = datetime.utcnow().replace(microsecond=0)

    # check if I'll be working the next 6 minutes
    response = requests.get(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'wsDateFromHours',
            'hrs': '0.1',
            'dt': now.isoformat(),
        }
    ).text
    bs = BeautifulSoup(response, 'xml')

    assert not bs.find('error')
    time = isodate.parse_datetime(bs.find('dt').getText()).replace(tzinfo=None)

    return time-now == timedelta(hours=0.1)

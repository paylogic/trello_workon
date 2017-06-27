"""Utility functions for getting data from Fogbugz."""
import requests
import datetime

import isodate
from bs4 import BeautifulSoup

FOGBUGZ_URL = 'https://paylogic.fogbugz.com/api.asp'


def check_errors(bs_obj, func_name):
    assert not bs_obj.find('error'), "Error in {0}: {1}".format(
        func_name,
        bs_obj.find('error').getText(),
    )


def is_in_schedule_time(fogbugz_token):
    now = datetime.datetime.utcnow().replace(microsecond=0)

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

    check_errors(bs, 'is_in_schedule_time')
    time = isodate.parse_datetime(bs.find('dt').getText()).replace(tzinfo=None)

    return time - now == datetime.timedelta(hours=0.1)


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

    check_errors(bs, 'get_current_est')

    if bs.find('hrsCurrEst'):
        return float(bs.find('hrsCurrEst').getText())
    else:
        return None


def set_current_est(fogbugz_token, case_number, estimate):
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'edit',
            'ixBug': case_number,
            'hrsCurrEst': str(estimate),
        }
    ).text
    bs = BeautifulSoup(response, 'xml')
    check_errors(bs, 'set_current_est')


def start_work_on(fogbugz_token, case_number):
    if not get_current_est(fogbugz_token, case_number):
        set_current_est(fogbugz_token, case_number, 1)
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'startWork',
            'ixBug': case_number,
        },
    ).text
    bs = BeautifulSoup(response, 'xml')
    check_errors(bs, 'start_work_on')


def stop_work(fogbugz_token):
    response = requests.post(
        url=FOGBUGZ_URL,
        params={
            'token': fogbugz_token,
            'cmd': 'stopWork',
        }
    ).text

    bs = BeautifulSoup(response, 'xml')
    check_errors(bs, 'stop_work')

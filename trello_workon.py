import requests

from util import trello_requests as tr, fogbugz_requests as fr

from models.user import User
from models.base import db_session

if __name__ == '__main__':
    print 'running trello_workon'

    boards = requests.get('http://10.0.30.52/dashboard/?format=json').json()

    user_case_number = {}

    for board_id in boards:
        # Get the data from trello.
        doing_list_id = tr.get_list_id_from_board_by_name(board_id, "Doing")
        fires_list_id = tr.get_list_id_from_board_by_name(board_id, "Fires")
        doing_cards = tr.get_doing_list_cards_from_board(doing_list_id)
        fires_cards = tr.get_doing_list_cards_from_board(fires_list_id)

        # Get the top card for each user in doing.
        user_cases = tr.get_top_card_for_users(doing_cards)

        # If there's anything in the Fires column for a user, assume (s)he's doing that, regardless of any card in
        # the "Doing" column.
        user_cases.update(tr.get_top_card_for_users(fires_cards))

        # Strip all superfluous info, like case name
        user_case_number.update(tr.get_user_case_number(user_cases))

    print 'got the following cases:'
    print user_case_number

    users = User.query.all()

    print 'will try for the following users'
    print users

    # Update all users, if applicable
    for user in users:
        fb_current_task = fr.get_working_on(user.fogbugz_token)

        # If the user is working on something, and it's not the current case, the user probably manually
        # changed the case (s)he's working on. in that case, don't change anything.
        # This allows the user to manually set a working on in FB, which isn't overridden by the tool
        # The user can then clear his working on in FB, and the tool will resume syncing trello and FB.
        if not fb_current_task in [0, user.current_case]:
            continue

        # If the user is either not working on anything, or still working on the case we assigned to him/her last time,
        # we can update what (s)he's working on with what's in trello.

        case_number = user_case_number.get(user.trello_user_id, 0)

        # We also need to check if it's within normal working hours for the user.
        if fr.is_in_schedule_time(user.fogbugz_token):
            if case_number != 0:
                fr.start_work_on(user.fogbugz_token, case_number)
                user.current_case = case_number
                print '{0} started work on {1}'.format(user.username, case_number)
            else:
                fr.stop_work_on(user.fogbugz_token, case_number)
                user.current_case = 0
                print '{0} stopped work on {1}'.format(user.username, case_number)

        else:  # Outside of schedule time, so stop working on the case.
            fr.stop_work_on(user.fogbugz_token, case_number)
            user.current_case = 0
            print '{0} stopped work on {1}, as it\'s the end of the workday'.format(user.username, case_number)

        db_session.commit()

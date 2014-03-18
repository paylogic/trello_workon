import requests

from util import trello_requests as tr, fogbugz_requests as fr

from models.user import User
from models.base import db_session
from models.board import Board

if __name__ == '__main__':
    print 'running trello_workon'

    board_ids = requests.get('http://10.0.30.52/dashboard/?format=json').json()

    boards = [Board(board_id) for board_id in board_ids]




    for board in boards:
        # Get the data from trello.


        # Get the top card for each user in doing.
        user_cases = tr.get_top_card_for_users(doing_cards)

        # If there's anything in the Fires column for a user, assume (s)he's doing that, regardless of any card in
        # the "Doing" column.
        user_cases.update(tr.get_top_card_for_users(fires_cards))

        # Strip all superfluous info, like case name
        user_case_number.update(tr.get_user_case_number(user_cases))
        for user in user_cases.keys():
            user_board[user] = board_id

    print 'user:board'
    print user_board

    print 'got the following cases:'
    print user_case_number

    users = User.query.all()

    print 'will try for the following users'
    print ', '.join([': '.join([user.username, user.trello_user_id]) for user in users])

    # Update all users, if applicable
    for user in users:

        if user.trello_user_id in user_board:

            user.board_id = user_board[user.trello_user_id]

        try:
            fb_current_task = fr.get_working_on(user.fogbugz_token)
        except AssertionError:
            print 'Something went wrong while getting the current fogbugz \'working on\' for {0}'.format(user.username)
            continue

        # If the user is working on something, and it's not the current case, the user probably manually
        # changed the case (s)he's working on. in that case, don't change anything.
        # This allows the user to manually set a working on in FB, which isn't overridden by the tool
        # The user can then clear his working on in FB, and the tool will resume syncing trello and FB.
        if fb_current_task in [0, user.current_case]:

            # If the user is either not working on anything, or still working on the case we assigned to him/her last time,
            # we can update what (s)he's working on with what's in trello.

            tr_current_task = user_case_number.get(user.trello_user_id, 0)


            # We also need to check if it's within normal working hours for the user.
            try:
                if fr.is_in_schedule_time(user.fogbugz_token):
                    if tr_current_task == fb_current_task:
                        print '{0} is still working on {1}'.format(user.username, tr_current_task)
                    elif tr_current_task != 0:
                        fr.start_work_on(user.fogbugz_token, tr_current_task)
                        user.current_case = tr_current_task
                        print '{0} started work on {1}'.format(user.username, tr_current_task)
                    else:
                        old_case = user.current_case
                        fr.stop_work_on(user.fogbugz_token, user.current_case)
                        user.current_case = 0
                        print '{0} stopped work on {1}'.format(user.username, old_case)

                else:  # Outside of schedule time, so stop working on the case.
                    fr.stop_work_on(user.fogbugz_token, tr_current_task)
                    user.current_case = 0
                    print '{0} stopped work on {1}, as it\'s the end of the workday'.format(user.username, tr_current_task)

            except AssertionError:
                print 'Something went wrong while updating the status of {0} on fogbugz'.format(user.username)

        else:
             print '{0} is currently working on a manually set case.'.format(user.username)

        fb_current_case = fr.get_working_on(user.fogbugz_token)
        case_name = fr.get_case_name(user.fogbugz_token, fb_current_case)
        if fb_current_case != 0:
            user.fogbugz_case = '{0}: {1}'.format(fb_current_case, case_name)
        else:
            user.fogbugz_case = ''

        db_session.commit()

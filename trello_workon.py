from util import trello_requests as tr, fogbugz_requests as fr

from models.user import User
if __name__ == '__main__':
    board_id = '52fdddb322b2909251d378db'

    # Get the data from trello
    list_id = tr.get_doing_list_id_from_board(board_id)
    cards = tr.get_doing_list_cards_from_board(list_id)
    user_cases = tr.get_top_doing_for_users(cards)
    user_cases = tr.get_user_case_number(user_cases)

    # Set the working on status in fogbugz
    for user_id, case_number in user_cases.iteritems():
        user = User.query().filter(User.trello_user_id == user_id).one()

        current_case = fr.get_working_on(user.fogbugz_token)

        # If the case that was set hasn't been changed, or the user isn't working on anything, set the case.
        # This allows the user to manually set a working on in FB, which isn't overridden by the tool
        # The user can then clear his working on in FB, and the tool will resume syncing trello and FB.
        if current_case == user.current_case or current_case == 0:
            fr.start_work_on(user.fogbugz_token, case_number)

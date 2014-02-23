from util import trello_requests as tr, fogbugz_requests as fr


if __name__ == '__main__':
    board_id = '52fdddb322b2909251d378db'
    list_id = tr.get_doing_list_id_from_board(board_id)
    cards = tr.get_doing_list_cards_from_board(list_id)
    user_cases = tr.get_top_doing_for_users(cards)
    users = tr.get_user_case_map(user_cases)
    print users

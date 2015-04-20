from flask import render_template, request, jsonify

from management.blueprint import management

from models.user import User, FogbugzTokenError, TrelloTokenError
from models.case import Case
from models.base import db_session


@management.route('/', methods=['GET', 'POST'])
def index():
    created = False
    error = False
    if request.method == 'POST':
        try:
            assert request.form['username'] != ''
            assert request.form['fogbugz_token'] != ''
            assert request.form['trello_token'] != ''
        except:
            error = "Not all fields were filled in!"
        else:
            try:
                user = User(
                    username=request.form['username'],
                    trello_token=request.form['trello_token'],
                    fogbugz_token=request.form['fogbugz_token'],
                )
                db_session.add(user)
                db_session.commit()
            except TrelloTokenError:
                error = "Invalid Trello token!"
            except FogbugzTokenError:
                error = "Invalid Fogbugz Token!"
            except Exception as e:
                error = "Unexpected error! {0}".format(repr(e))
            else:
                created = True
    return render_template('submit.html', created=created, error=error)


@management.route('/board/<board_id>')
def board_users(board_id):
    users = User.query.filter(User.board_id == board_id).all()
    cases = dict(
        [
            (case.case_number, case) for case in
            Case.query.filter(
                Case.case_number.in_([user.current_case for user in users])
            ).all()
        ]
    )
    result = {}
    for user in users:
        result[user.username] = {
            'case': user.fogbugz_case,
        }
        if user.current_case and user.current_case in cases:
            result[user.username]['todo'] = cases[user.current_case].todo_sum
            result[user.username]['doing'] = cases[user.current_case].doing_sum
            result[user.username]['done'] = cases[user.current_case].done_sum

    return jsonify(result)

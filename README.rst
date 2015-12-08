trello_workon
=============

Syncs Trello's "Doing" column with Fogbugz' "Working on" system

This is a major refactor of the original system. The tool uses the Trello column id of the "Doing" column and the specific board id. These should be configured in a settings.py file.

The settings.py file should contain:

::

	TRELLO_TOKEN = ''
	TRELLO_APP_ID = ''
	BOARD_ID = ''
	DOING_LIST_ID = ''

The system consists of two parts, the workon sync, and the management server.

The workon sync is run via cron, e.g.:

::

    */5 * * * * /srv/sites/trello_workon/trello_workon/trello_workon.sh

The management server is run using gunicorn:

::

    /srv/sites/trello_workon/trello_workon/.env/bin/gunicorn -c /srv/sites/trello_workon/gunicorn_config.py /srv/sites/trello_workon/trello_workon


Development environment:

::

    make develop
    # optionally you can activate venv
    source .env/bin/activate


Deployment:

::

    fab -u <your username> deploy:pypi_index=<your pypi index>

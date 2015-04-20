trello_workon
=============

Syncs Trello's "Doing" column with Fogbugs' "Working on" system

This is a major refactor of the original system.

The system consists of two parts, the workon sync, and the management server.

The workon sync is run via cron, e.g.:

	*/5 * * * * /srv/sites/trello_workon/trello_workon/trello_workon.sh

The management server is run using gunicorn:

	/srv/sites/trello_workon/trello_workon/.env/bin/gunicorn -u www-data -c /srv/sites/trello_workon/gunicorn_config.py /srv/sites/trello_workon/trello_workon

Known bugs:

- Fires can sometimes malfunction, causing the system to lose track and revert to manual mode


#!/bin/bash
. /srv/sites/trello_workon/env.sh
cd /srv/sites/trello_workon/trello_workon
exec /srv/sites/trello_workon/trello_workon/.env/bin/gunicorn -u deploy -c gunicorn_config.py management.wsgi

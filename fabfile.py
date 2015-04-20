"""
Fabric deployment script

"""

from fabric.api import task, run, cd

env.hosts = ['10.0.31.52']


@task
def deploy():
    """Deploy the current version on github to the server."""

    cd('/srv/sites/trello_workon/trello_workon')
    run('git pull')
    run('virtualenv .env')
    run('. .env/bin/activate')
    run('pip install -r requirements.txt')
    cd('sudo service trello_workon restart')

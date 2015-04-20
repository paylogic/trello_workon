"""
Fabric deployment script

"""

from fabric.api import env, task, run, cd, sudo

env.hosts = ['10.0.31.52']
user = 'deploy'

@task
def deploy():
    """Deploy the current version on github to the server."""

    with cd('/srv/sites/trello_workon/trello_workon'):
        sudo('git pull', user=user)
        sudo('virtualenv .env', user=user)
        sudo('.env/bin/pip install -r requirements.txt', user=user)
        sudo('service trello_workon restart')

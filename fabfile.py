"""
Fabric deployment script

"""

from fabric.api import task, run


env.hosts = ['10.0.30.52']

@task
def deploy():
	"""Deploy the current version on github to the server."""

	# TODO: stop server

	cd('/srv/sites/trello_workon/trello_workon')
	run('git pull')
	run('virtualenv .env')
	run('. .env/bin/activate')
	run('pip install -r requirements.txt')

	# TODO: start server

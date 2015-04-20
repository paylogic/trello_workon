# create virtual environment
.env:
	virtualenv .env

# install all needed for development
develop: .env
	.env/bin/pip install -r requirements-dev.txt

# clean the development envrironment
clean:
	-rm -rf .env

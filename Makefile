#
# Basic makefile for general targets
#

EASY_INSTALL = bin/easy_install
DEV_ENV = source bin/activate ;
NOSE = bin/nosetests --nocapture
NOSY = bin/nosy
PYTHON_PATH = PYTHONPATH=goalltheplaces
PIP = bin/pip
PYTHON = $(ENV) bin/python

## Testing ##
.PHONY: test tdd dist docs clean requirements virtualenv
test:
	$(NOSE) tests

tdd:
	$(NOSY)

docs:
	bin/sphinx-build -b html -d docs/build/doctrees docs/source docs/html

foreman_streamers:
	$(DEV_ENV) foreman start -f Procfile.streamers

foreman_workers:
	$(DEV_ENV) foreman start -f Procfile.workers

foreman_producers:
	$(DEV_ENV) foreman start -f Procfile.producers

develop:
	$(PYTHON) setup.py develop

clean:
	-$(PYTHON) setup.py clean
	# clean python bytecode files
	-find . -type f -name '*.pyc' -o -name '*.tar.gz' -delete
	-rm -f nosetests.xml
	-rm -f pip-log.txt
	-rm -f .nose-stopwatch-times
	-rm -rf build dist *.egg-info

dist: clean
	$(shell export COPYFILE_DISABLE=true)

	$(PYTHON) setup.py sdist

requirements:
	$(EASY_INSTALL) -U distribute
	$(PIP) install -r requirements.pip
	-rm README.txt
	# These libs don't work when installed via pip.
	$(EASY_INSTALL) nose_machineout
	$(EASY_INSTALL) readline

osx_requirements:
	brew install zeromq

virtualenv:
	virtualenv --distribute .


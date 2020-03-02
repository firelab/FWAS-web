
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python


venv/bin/activate: requirements.in dev-requirements.in
	test -f venv/bin/activate || virtualenv -p $(shell which python3) venv
	venv/bin/pip install -Ur requirements.txt ;\
	venv/bin/pip install -Ur dev-requirements.txt ;\
	touch venv/bin/activate 

.PHONY: run
test: venv/bin/activate
	pytest tests/

.PHONY: lock
lock: 
	pip-compile requirements.in > requirements.txt
	pip-compile dev-requirements.in > dev-requirements.txt

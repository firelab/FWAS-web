
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python


venv/bin/activate: requirements.in dev-requirements.in
	rm -rf venv/
	test -f venv/bin/activate || virtualenv -p $(shell which python3) venv
	. venv/bin/activate ;\
	pip-compile requirements.in > requirements.txt ;\
	pip-compile dev-requirements.in > dev-requirements.txt ;\
	pip install -Ur requirements.txt ;\
	pip install -Ur dev-requirements.txt ;\
	touch venv/bin/activate 

.PHONY: run
test: venv/bin/activate
	${PYTHON} pytest tests/

.PHONY: lock
lock: 
	pip-compile requirements.in > requirements.txt
	pip-compile dev-requirements.in > dev-requirements.txt

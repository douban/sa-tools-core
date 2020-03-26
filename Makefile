SHELL = bash

.PHONY : clean_pyc install init test

clean_pyc:
	@find . -name "*.pyc" -exec rm {} +

venv:
	@python3.7 -mvenv venv
	@source venv/bin/activate; pip install --upgrade pip

install: venv
	@source venv/bin/activate; pip install -e .[script]

venv2:
	@virtualenv venv2
	@source venv2/bin/activate; pip install --upgrade pip

install2: venv2
	@source venv2/bin/activate; pip install -e .[script]

test:
	@python setup.py test

clean:
	@rm -rf dist build

dist: clean
	@source venv/bin/activate; pip install --upgrade setuptools wheel
	@source venv/bin/activate; python3 setup.py sdist bdist_wheel

publish: dist
	@source venv/bin/activate; pip install --upgrade twine
	@source venv/bin/activate; twine upload dist/*

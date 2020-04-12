.PHONY : clean install init test dist publish

install:
	@source venv/bin/activate; pip install -e .

init: new_venv
	@python -m venv venv
	@source venv/bin/activate; pip install --upgrade pip
	$(MAKE) install

test:
	@python setup.py test

clean:
	@rm -rf dist build
	@find . -name "*.pyc" -exec rm {} +
	@find . -name __pycache__ -exec rm -r {} +

dist: clean
	@source venv/bin/activate; pip install --upgrade setuptools wheel
	@source venv/bin/activate; python setup.py sdist bdist_wheel

publish: dist
	@source venv/bin/activate; pip install --upgrade twine
	@source venv/bin/activate; twine upload dist/*

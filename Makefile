.PHONY : clean_pyc new_venv install init test

clean_pyc:
	@find . -name "*.pyc" -exec rm {} +

new_venv:
	@virtualenv venv

install:
	@source venv/bin/activate; pip install -e . --process-dependency-links --trusted-host github.intra.douban.com --trusted-host code.dapps.douban.com

init: new_venv
	@source venv/bin/activate; pip install --upgrade pip
	$(MAKE) install

test:
	@python setup.py test

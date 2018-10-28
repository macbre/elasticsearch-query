coverage_options = --include='wikia_common_kibana.py' --omit='test/*'

install:
	pip install -e .[dev]

test:
	pytest -v

coverage:
	rm -f .coverage*
	rm -rf htmlcov/*
	coverage run -p -m pytest -v
	coverage combine
	coverage html -d htmlcov $(coverage_options)
	coverage xml -i
	coverage report $(coverage_options)

lint:
	pylint wikia_common_kibana.py

publish:
	# run git tag -a v0.0.0 before running make publish
	python setup.py sdist upload -r pypi

.PHONY: test

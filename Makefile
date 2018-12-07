coverage_options = --include='elasticsearch_query.py' --omit='test/*'

install:
	pip install -e .[dev]

test:
	pytest -vv

coverage:
	rm -f .coverage*
	rm -rf htmlcov/*
	coverage run -p -m pytest -vv
	coverage combine
	coverage html -d htmlcov $(coverage_options)
	coverage xml -i
	coverage report $(coverage_options)

lint:
	pylint elasticsearch_query.py

publish:
	# run git tag -a v0.0.0 before running make publish
	python setup.py sdist
	twine upload --skip-existing dist/*

.PHONY: test

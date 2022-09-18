.PHONY: tests, coverage, lint, release

tests:
	python -m unittest

coverage:
	python -m coverage erase
	python -m coverage run --source=cutie -m unittest
	python -m coverage report
	python -m coverage html
	coveralls

black:
	black *.py

release: black, tests
	python setup.py sdist bdist_wheel
	twine upload dist/*

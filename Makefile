.PHONY: tests, coverage

tests:
	python -m unittest

coverage:
	python -m coverage erase
	python -m coverage run --source=cutie -m unittest
	python -m coverage report
	python -m coverage html

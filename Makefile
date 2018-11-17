.PHONY: tests, coverage

tests:
	python -m unittest

coverage:
	python3.7 -m coverage erase
	python3.7 -m coverage run --source=cutie -m unittest
	python3.7 -m coverage report
	python3.7 -m coverage html

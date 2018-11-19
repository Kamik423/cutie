.PHONY: tests, coverage, lint, release

tests:
	python -m unittest

coverage:
	python -m coverage erase
	python -m coverage run --source=cutie -m unittest
	python -m coverage report
	python -m coverage html

lint:
	pylint setup.py cutie.py examples.py --score=no --disable=R0912,R0913,R0914,R0915,C0103
	flake8 setup.py cutie.py examples.py
	pycodestyle setup.py cutie.py examples.py

release: tests, lint
	python setup.py sdist bdist_wheel
	twine upload dist/*

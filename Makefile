.PHONY: tests, coverage

tests:
	python -m unittest

coverage:
<<<<<<< HEAD
	python -m coverage erase
	python -m coverage run --source=cutie -m unittest
	python -m coverage report
	python -m coverage html
=======
	python3.7 -m coverage erase
	python3.7 -m coverage run --source=cutie -m unittest
	python3.7 -m coverage report
	python3.7 -m coverage html
>>>>>>> 124c738e2d8dccaee8893e48072d35b59200ba8d

#!/bin/bash

echo "Starting lint on setup.py"
pylint setup.py --score=no --disable=R0912,R0913,R0914,R0915,C0103
pycodestyle setup.py
flake8 setup.py

echo "Starting lint on cutie.py"
pylint cutie.py --score=no --disable=R0912,R0913,R0914,R0915,C0103
pycodestyle cutie.py
flake8 cutie.py

echo "Starting lint on example.py"
pylint example.py --score=no --disable=R0912,R0913,R0914,R0915,C0103
pycodestyle example.py
flake8 example.py

echo "Finished linting all files"

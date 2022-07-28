# Testing report
This document details the results of testing the program

## Unit testing
Unit testing is done with automated tests using Pytest ([Unit test coverage report](https://jonathanheyno.github.io/tiramarkovchaincodecov/index.html)). The overall test coverage is currently 98%

If you want to run the tests locally:
1) install the dependencies in [requirements_dev.txt](/../requirements_dev.txt) with `pip install requirements_dev.txt`
2a) to get the test coverage, run `coverage report -m` in the project root folder
2b) if instead you want a html version of the coverage report:
	- run command `coverage run --branch -m pytest src`
	- then run `coverage html`. The report will be created into the folder `htmlcov`

## Code quality
Code quality in this project is measured with Pylint according to the definitions in the file [.pylintrc](/../.pylintrc). The score for code quality is currently 9.66.

To run the Pylint check locally:
1) install the dependencies in [requirements_dev.txt](/../requirements_dev.txt) with `pip install requirements_dev.txt`
2) run the command `pylint src` in the project root folder

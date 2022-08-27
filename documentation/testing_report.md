# Testing report
This document details the results of testing the program

## Unit testing
Unit testing is done with automated tests using Pytest ([Unit test coverage report](https://jonathanheyno.github.io/tiramarkovchaincodecov/index.html)). The overall test coverage is currently 97%

![coverage report](./pics/coverage_report.png)

If you want to run the tests locally:
1) install the dependencies in [requirements_dev.txt](../requirements_dev.txt) with `pip install -r requirements_dev.txt`
2) to get the test coverage, run `pytest src`, then run `coverage report -m` in the project root folder
2) if instead you want a html version of the coverage report:
	- run command `coverage run --branch -m pytest src`
	- then run `coverage html`. The report will be created into the folder `htmlcov`

## Manual testing

The program is tested with different texts, and quality of generated text is evaluated according to contents and grammatical structure.

The results are in line with expectations.

The quality of the text is directly related to the order of the Markov chain. Increasing the order of the Markov chain results
in better quality text, but also in more closely repeating the source data.

A larger input file also results in more unique sentences

## Code quality
Code quality in this project is measured with Pylint according to the definitions in the file [.pylintrc](../.pylintrc). The score for code quality is currently 9.30.

To run the Pylint check locally:
1) install the dependencies in [requirements_dev.txt](../requirements_dev.txt) with `pip install -r requirements_dev.txt`
2) run the command `pylint src` in the project root folder

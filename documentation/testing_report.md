# Testing report
This document details the results of testing the program

## Unit testing
Unit testing is done with automated tests using Pytest ([Unit test coverage report](https://jonathanheyno.github.io/tiramarkovchaincodecov/index.html)). The overall test coverage is currently 83%

If you want to run the tests locally:
1) install the dependencies in [requirements_dev.txt](../requirements_dev.txt) with `pip install -r requirements_dev.txt`
2) to get the test coverage, run `pytest src`, then run `coverage report -m` in the project root folder
2) if instead you want a html version of the coverage report:
	- run command `coverage run --branch -m pytest src`
	- then run `coverage html`. The report will be created into the folder `htmlcov`

## Manual testing

The program is tested with different texts, and quality of generated text is evaluated according to contents and grammatical structure.

Changing the order of the Markov chain to 3 and abandoning the idea of following a given sentence structure has improved the
quality of the generated text. Given that we are reading in quite large bodies of text, this works quite well and we are not
just repeating the source data.

## Code quality
Code quality in this project is measured with Pylint according to the definitions in the file [.pylintrc](../.pylintrc). The score for code quality is currently 8.12.

To run the Pylint check locally:
1) install the dependencies in [requirements_dev.txt](../requirements_dev.txt) with `pip install -r requirements_dev.txt`
2) run the command `pylint src` in the project root folder

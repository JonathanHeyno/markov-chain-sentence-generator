# User guide


## Running the program
This program runs with Python, which needs to be installed.

1) Clone the repository
2) No additional dependencies need to be installed. If you want to run the unit tests and Pylint and don't have them installed, install those dependencies from [requirements_dev.txt](../requirements_dev.txt) with the command `pip install -r requirements_dev.txt`.
3) Run command `python src/index.py` in the root

## Using the program
The program uses a text interface.

1) Put the text file (e.g. 'my_text.txt') that will be read into the `sourcedata` folder
2) Tell the program to read in the file (that is in the `sourcedata` folder). There are a few text files you can use for testing, some quite big, for instance 'sherlock_holmes.txt'.
3) The default order of the Markov chain is 3. Change it if you want something else.
4) You can now generate text. Give the program a maximum amount of words to generate.

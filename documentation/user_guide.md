# User guide


## Running the program
This program runs with Python, which needs to be installed.

1) Clone the repository
2) Install the dependencies from [requirements.txt](../requirements.txt) using command`pip install -r requirements.txt`. If you also want to run the unit tests and Pylint, use file [requirements_dev.txt](../requirements_dev.txt) instead.
3) Run command `python src/index.py` in the root

## Using the program
The program uses a text interface. Currently it is able to read in a given text file, generate a trie structure and search for a list of words determined by the order of the Markov chain.

1) Put the text file (e.g. 'text_for_pytest.txt') that will be read into the `sourcedata` folder
2) Tell the program to read in the file
3) The default order of the Markov chain is 2. Change it if you want something else
4) Tell the program to create the trie structure
5) You can now generate text. Give the program a maximum amount of words to generate.

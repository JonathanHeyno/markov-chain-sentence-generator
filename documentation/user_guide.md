# User guide


## Running the program
This program runs with Python, which needs to be installed.

1) Clone the repository
2) Install the dependencies from [requirements.txt](../requirements.txt) using command`pip install -r requirements.txt`. If you also want to run the unit tests and Pylint, use file [requirements_dev.txt](../requirements_dev.txt) instead.
3) Run command `python src/index.py` in the root

## Using the program
The program uses a text interface.

1) Put the text file (e.g. 'my_text.txt') that will be read into the `sourcedata` folder
2) Tell the program to read in the file (that is in the `sourcedata` folder). There are a few text files you can use for testing, some quite big, for instance 'sherlock_holmes.txt'.
3) The default order of the Markov chain is 3. Change it if you want something else.
4) Tell the program to create the trie structure. Note, whenever you change the order of the Markov chain (step 3), you must recreate the trie (step 4).
5) You can now generate text. Give the program a maximum amount of words to generate.

import re
from pathlib import Path
from nltk.tokenize import wordpunct_tokenize
from config import SOURCE_FILE_PATH
from trie import trie


class Service():

    def __init__(self):
        self._text= []
        self._source_file = ''
        self._order = 2

    @property
    def source_file(self):
        return self._source_file

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if value != self._order:
            trie.reset()
        self._order = int(value)

    def read_source_file(self, filename):
        """Reads in a new text file ignoring special characters and numbers,
        and forms an array of the words

        Args:
            filename (string): the name of the file in 'sourcedata' folder

        Returns:
            string: message about succesfully reading the file or failing
        """
        filepath = SOURCE_FILE_PATH+filename
        if not Path(filepath).is_file():
            return 'FILE ' + filename + ' WAS NOT FOUND IN ' + filepath

        self._text = []
        trie.reset()
        with open(filepath, encoding='utf-8') as file:
            for line in file:
                chars_to_remove = "_\"+'{}()?!.,:;*&@$#[]-^-\\"
                line = line.lower()
                line = line.strip()
                line= re.sub(rf'[{chars_to_remove}]', '', line)
                tokens = wordpunct_tokenize(line)
                for token in tokens:
                    if token.isalpha():
                        self._text.append(token)
        self._source_file = filename
        return '\n\nFILE READ\n'


    def create_trie_and_count_frequencies(self):
        """Creates a new trie from the text file that was read in with a depth determined
        by the order of the Markov chain. Adds to the lowest layer the number of times the
        trie branch has occurred in the source text

        Returns:
            string: a message on the success or failure of creating the trie
        """
        num_words = len(self._text)
        if num_words <= self._order:
            return '\nORDER OF MARKOV CHAIN LARGER THAN WORD COUNT IN SOURCE FILE\n'

        trie.reset()

        # Insert a word + the next n words into the trie
        # repeat for all words in source text file
        index = 0
        while index + self._order < num_words:
            words = []
            for i in range(self._order + 1):
                words.append(self._text[index + i])
            trie.insert_words_and_increase_frequency(words)
            index += 1
        return '\nTRIE CREATED\n'



    def search_trie(self, words):
        """Searches the trie for the given list of words

        Args:
            words (array): word list to be located from the tree

        Returns:
            integer: the amount of times the word list has occurred in the source text
        """
        last_node = trie.search(words)
        if not last_node:
            return 0
        return last_node.frequency

service = Service()

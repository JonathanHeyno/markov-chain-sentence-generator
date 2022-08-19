from random import choice
from node import Node

class Trie():

    def __init__(self):
        self._root = Node()

    def reset(self):
        self._root = Node()

    def insert_words_and_increase_frequency(self, words, stop_words='_NONE_'):
        """Creates an entry for the word list if needed and increases
        the amount of times it has been given

        Args:
            words (array): word list given to the trie
        """
        if not stop_words:
            stop_words = '_NONE_'
        node = self._root
        for word in words:
            node = node.insert_and_return_child_node(word)
            node.increase_word_frequency()
        # For the last node we also maintain the frequencies of stop words
        # that came before it
        node.increase_stop_word_frequency(stop_words)


    def traverse(self, words):
        """Traverses the trie for the given word list

        Args:
            words (array): the word list to be traversed through the trie

        Returns:
            Node: the node of the last word in the list or None
        """
        if not words:
            return self._root
        node = self._root
        for word in words:
            node = node.get_child_node(word)
            if not node:
                return None
        return node

    def choose_initial_words(self, amount_of_words):
        node = self._root
        initial_words = []
        for _ in range(amount_of_words):
            word, node = node.choose_any_child()
            if not node:
                return []
            initial_words.append(word)
        return initial_words



    # Selects a word + stop words.
    def get_next_word(self, base_words):
        next_word = ''
        stop_words = '_NONE_'
        node_of_last_word = self.traverse(base_words)
        if node_of_last_word:
            next_word, stop_words = node_of_last_word.select_next_word()
        return next_word, stop_words

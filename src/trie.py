from random import choice
from node import Node

class Trie():

    def __init__(self):
        self._root = Node()

    def reset(self):
        self._root = Node()

    def insert_words_and_increase_frequency(self, words):
        """Creates an entry for the word list if needed and increases
        the amount of times it has been given

        Args:
            words (array): word list given to the trie
        """
        node = self._root
        for word in words:
            node = node.insert_and_return_child_node(word[0], word[1])
            node.increase_word_frequency()


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
        taso = 0
        for word in words:
            node = node.get_child_node(word)
            if not node:
                return None
            taso += 1
        return node


    def choose_initial_words(self, amount_of_words, sentence_structure):
        initial_structure = sentence_structure[:(amount_of_words+1)]
        word_list = self._root.get_word_chains_with_structure(initial_structure)
        chose_words = choice(word_list)[:amount_of_words]
        return chose_words

    # Selects a word of given type (e.g. verb) based on previous words.
    # If e.g. we need to select a verb based on the two previous words,
    # but those two words are never followed by a verb in the input text,
    # we drop the first word away and try finding a verb that follows
    # the second word, and if that doesn't work, we go get a verb
    # from the root node.
    def get_next_word(self, base_words, next_word_pos):
        next_word = ''
        amount_of_words = len(base_words)

        node_of_last_word = self.traverse(base_words)
        if node_of_last_word:
            next_word = node_of_last_word.select_next_word(next_word_pos)
        if next_word:
            return next_word

        while not next_word:
            amount_of_words -= 1
            if amount_of_words == -1:
                return 'ERROR!!!!'
            if amount_of_words == 0:
                node_of_last_word = self._root
            else:
                base_words = base_words[1:]
                node_of_last_word = self.traverse(base_words)

            if node_of_last_word:
                next_word = node_of_last_word.select_next_word(next_word_pos)
            if next_word:
                return next_word

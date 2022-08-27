from node import Node

class Trie():

    def __init__(self):
        self._root = Node()

    def reset(self):
        self._root = Node()

    def insert_words_and_increase_frequency(self, words, stop_words='_NONE_', preceded_by='_NONE_', followed_by='_NONE_'):
        """Creates an entry for the word list if needed and increases
        the amount of times it has been given

        Args:
            words (array): word list given to the trie
        """
        if not stop_words:
            stop_words = '_NONE_'
        if not preceded_by:
            preceded_by = '_NONE_'
        if not followed_by:
            followed_by = '_NONE_'

        node = self._root
        for word in words:
            node = node.insert_and_return_child_node(word)
            node.increase_word_frequency()

        node.increase_stop_word_frequency(stop_words)
        node.increase_preceded_by_frequency(preceded_by)
        node.increase_followed_by_frequency(followed_by)


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
        """Selects initial words from the trie to start the Markov chain

        Args:
            amount_of_words (int): The amount of words to be selected 

        Returns:
            array, array: an array of words and their corresponding nodes in the trie
        """
        node = self._root
        initial_words = []
        initial_nodes = []
        for _ in range(amount_of_words):
            word, node = node.choose_any_child()
            if not node:
                return [], []
            initial_words.append(word)
            initial_nodes.append(node)
        return initial_words, initial_nodes



    def get_next_word(self, base_words):
        """Selects the next word for the Markov process

        Args:
            base_words (array): The previous words based on which
            the next word from the trie is selected

        Returns:
            string, Node: the next word and its corresponding node
        """
        next_word = ''
        node_of_last_word = self.traverse(base_words)
        if node_of_last_word:
            next_word, node_of_last_word = node_of_last_word.select_next_word()
        return next_word, node_of_last_word

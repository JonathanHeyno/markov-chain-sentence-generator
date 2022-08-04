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
            node = node.insert_and_return_child_node(word)
        node.increase_word_frequency()


    def traverse(self, words):
        """Traverses the trie for the given word list

        Args:
            words (array): the word list to be traversed through the trie

        Returns:
            Node: the node of the last word in the list or None
        """
        node = self._root
        for word in words:
            node = node.get_child_node(word)
            if not node:
                return None
        #if node.frequency > 0:
        #    return node
        #return None
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


    def get_next_word(self, base_words):
        node_of_last_word = self.traverse(base_words)
        return node_of_last_word.select_next_word()



trie = Trie()

class Node():

    def __init__(self):
        self.next_words = {}
        self._frequency = 0

    @property
    def frequency(self):
        return self._frequency

    def get_child_node(self, word):
        return self.next_words.get(word)

    def insert_and_return_child_node(self, word):
        """Creates the child node corresponding to the given word if not yet created

        Args:
            word (string): the word for which a child node will be retrieved

        Returns:
            Node: the child node corresponding to the given word
        """
        next_node = self.next_words.get(word)
        if next_node:
            return next_node
        new_node = Node()
        self.next_words[word] = new_node
        return new_node


    def increase_word_frequency(self):
        """increases the amount of times this node has occurred as the last node in a list of words
        """
        self._frequency += 1

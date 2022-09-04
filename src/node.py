import random

class Node():

    def __init__(self):
        self.next_words = {}
        self._frequency = 0
        self.stop_words = {}
        self.preceded_by = {}
        self.followed_by = {}


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

    def increase_stop_word_frequency(self, stop_words = '_NONE_'):
        """increases the amount of times the stop word has occurred before this word
        """
        if not stop_words:
            stop_words = '_NONE_'
        self.stop_words[stop_words] = self.stop_words.get(stop_words, 0) + 1

    def increase_preceded_by_frequency(self, preceded_by = '_NONE_'):
        """increases the amount of times a punctuation .?!, has occurred before this word
        """
        if not preceded_by:
            preceded_by = '_NONE_'
        self.preceded_by[preceded_by] = self.preceded_by.get(preceded_by, 0) + 1

    def increase_followed_by_frequency(self, followed_by = '_NONE_'):
        """increases the amount of times a punctuation .?!, has followed this word
        """
        if not followed_by:
            followed_by = '_NONE_'
        self.followed_by[followed_by] = self.followed_by.get(followed_by, 0) + 1

    def choose_any_child(self):
        """Selects a child randomly

        Returns:
            tuple: the selected word and its coresponding node
        """
        if not self.next_words:
            return '', None
        return random.choice(list(self.next_words.items()))


    def select_next_word(self):
        """Selects a child according to child nodes' frequencies

        Returns:
            String, Node: the selected word and its corresponding node
        """
        words = []
        cumulative_weights = []

        cum_weight = 0
        for word, node in self.next_words.items():
            words.append((word, node))
            cumulative_weights.append(cum_weight + node.frequency)
            cum_weight += node.frequency
        if not words:
            return '', None
        selected = random.choices(words, cum_weights=cumulative_weights)
        return selected[0][0], selected[0][1]

import random

class Node():

    def __init__(self, part_of_speech=''):
        self.next_words = {}
        self._frequency = 0
        self._part_of_speech = part_of_speech
        self.stop_words = {}

    @property
    def part_of_speech(self):
        return self._part_of_speech

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
        if not stop_words:
            stop_words = '_NONE_'
        self.stop_words[stop_words] = self.stop_words.get(stop_words, 0) + 1


    def choose_any_child(self):
        if not self.next_words:
            return '', None
        return random.choice(list(self.next_words.items()))

    # Selects a child according to their frequencies
    # and associated stop words by frequencuies.
    def select_next_word(self,):
        words = []
        cumulative_weights = []

        cum_weight = 0
        for word, node in self.next_words.items():
            words.append((word, node))
            cumulative_weights.append(cum_weight + node.frequency)
            cum_weight += node.frequency
        if not words:
            return '', '_NONE_'
        selected = random.choices(words, cum_weights=cumulative_weights)
        stop_words = selected[0][1].select_stop_words()
        return selected[0][0], stop_words


    def select_stop_words(self):
        words = []
        cumulative_weights = []

        cum_weight = 0
        for word, frequency in self.stop_words.items():
            words.append(word)
            cumulative_weights.append(cum_weight + frequency)
            cum_weight += frequency

        selected = random.choices(words, cum_weights=cumulative_weights)
        return selected[0]

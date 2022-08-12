import random

class Node():

    def __init__(self, part_of_speech=''):
        self.next_words = {}
        self._frequency = 0
        self._part_of_speech = part_of_speech

    @property
    def part_of_speech(self):
        return self._part_of_speech

    @property
    def frequency(self):
        return self._frequency

    def get_child_node(self, word):
        return self.next_words.get(word)

    # Get all chains below this node that follow a given structure (e.g. pronoun - verb - preposition)
    def get_word_chains_with_structure(self, structure):
        if not structure:
            return []

        structure_length = len(structure)

        if structure_length == 1:
            word_list = []
            for word, node in self.next_words.items():
                if node.part_of_speech == structure[0]:
                    word_list.append([word])
            return word_list

        word_chains = []
        for word, node in self.next_words.items():
            if node.part_of_speech == structure[0]:
                all_returned_chains = node.get_word_chains_with_structure(structure[1:])
                for returned_chain in all_returned_chains:
                    new_word_chain = [word]
                    new_word_chain += returned_chain
                    word_chains.append(new_word_chain)
        return word_chains




    def insert_and_return_child_node(self, word, part_of_speech=''):
        """Creates the child node corresponding to the given word if not yet created

        Args:
            word (string): the word for which a child node will be retrieved

        Returns:
            Node: the child node corresponding to the given word
        """
        next_node = self.next_words.get(word)
        if next_node:
            return next_node
        new_node = Node(part_of_speech)
        self.next_words[word] = new_node
        return new_node


    def increase_word_frequency(self):
        """increases the amount of times this node has occurred as the last node in a list of words
        """
        self._frequency += 1


    def choose_any_child(self):
        if not self.next_words:
            return '', None
        return random.choice(list(self.next_words.items()))

    # Selects a child according to their frequencies that have a given part of speech,
    # e.g. select a child that is a verb.
    def select_next_word(self, part_of_speech):
        words = []
        cumulative_weights = []

        cum_weight = 0
        for word, node in self.next_words.items():
            if node.part_of_speech == part_of_speech:
                words.append(word)
                cumulative_weights.append(cum_weight + node.frequency)
                cum_weight += node.frequency
        if not words:
            return ''
        word = random.choices(words, cum_weights=cumulative_weights)
        return word[0]

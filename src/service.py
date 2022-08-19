from random import choice
import re
from pathlib import Path
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
from nltk.tag import pos_tag, map_tag
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords
from config import SOURCE_FILE_PATH
from trie import Trie


class Service():

    def __init__(self):
        self._text= []
        self._source_file = ''
        self._order = 3
        self._word_trie = Trie()


    @property
    def source_file(self):
        return self._source_file

    @property
    def order(self):
        return self._order

    @property
    def order_sentence_structure(self):
        return self._order_sentence_structure

    @order.setter
    def order(self, value):
        if value != self._order:
            self._word_trie.reset()
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
        self._word_trie.reset()

        print('\n\nReading file '+filename)


        # Needs to be refactored. Basically here we read in the file, clean it up (= remove special characters, etc.)
        # Most of the messy logic deals with the different ways of handling the characters " and ' since they usually
        # create sentences inside of other sentences, and the character ' is additionally used as a genitive,
        # e.g. Bob's house.

        # We also break the text up into sentences and perform part of speech tagging, and store the different
        # sentence structures, e.g. "pronoun - verb - preposition - adjective - noun..."
        with open(filepath, encoding = 'utf-8') as f:
            text = []
            print('\nCleaning text...')
            chars_to_remove = "0123456789_\"+{}(),:;*&@$#[]-^-\\"
            special_words = {"Mr.": "Mr", "Dr.": "Dr", "Mrs.": "Mrs", "Ms.": "Ms", "Prof.": "Prof", "E.g.": "Eg", "I.e.": "Ie", "etc.": "etc", "i.e.": "ie", "e.g.": "eg"}
            previous_word = 'a'
            for line in f:
                line = line.strip()
                # Maybe not good idea to make lower because then names may become nouns
                #line = line.lower()
                words = line.split()
                for word in words:

                    # This logic is for separating two pieces of texts that are in quotations into separate sentences, e.g.
                    # two characters talking:
                    # "Is that you, Holmes?"
                    # "No, it is I, Douglas"
                    if previous_word and (previous_word[-1] == '"' or previous_word[-1] == "'") and (word[0] == '"' or word[0] == "'"):
                        text.pop(-1)
                        corrected_previous_word = previous_word[:-1]
                        while len(previous_word)>1 and (corrected_previous_word[0] == "'" or corrected_previous_word[0] == '"'):
                            corrected_previous_word = corrected_previous_word[1:]
                        new_previous_word = ''
                        for char in corrected_previous_word:
                            if not char in chars_to_remove:
                                new_previous_word += char
                        text.append(new_previous_word)
                    if previous_word[-1] == '-':
                        text.pop(-1)
                        word = previous_word[:-1] + word
                    previous_word = word[:]
                    cleaned_word = ''
                            # If the previous word was part of a quote in the middle of the sentence, e.g.
                            # He asked "What is this?", pointing to the TV.
                            # We need to also remove the ? (or !)
                    if len(word) > 1 and (word[-2:] == '!"' or word[-2:] == '?"'):
                        word = word[:-2]
                    previous_char = 'a'
                    for char in word:
                        # pretty rare, but we replace e.g.
                        # No--but who are you
                        # --> No but who are you?
                        if char == '-' and previous_char == '-':
                            char = ' '
                        previous_char = char
                        if not char in chars_to_remove:
                            cleaned_word += char
                    if cleaned_word:
                        if cleaned_word[0] == "'":
                            cleaned_word = cleaned_word[1:]
                        if cleaned_word and cleaned_word[-1] == "'":
                            # If the previous word was part of a quote in the midle of the sentence, e.g.
                            # He asked 'What is this?', pointing to the TV.
                            # We need to also remove the ? (or !)
                            if len(cleaned_word) > 1 and cleaned_word[-2] in "!.?":
                                cleaned_word = cleaned_word[:-2]
                        # We do not remove the apostrophe if it is the plural genitive, e.g.
                        # the Smiths' house was renovated last year
                        if cleaned_word and cleaned_word[-1] == "'":
                            if len(cleaned_word) > 1 and not cleaned_word[-2] == "s":
                                cleaned_word = cleaned_word[:-1]
                        if cleaned_word in special_words:
                            text.append(special_words.get(cleaned_word).lower())
                        else:
                            text.append(cleaned_word.lower())


            print('Tokenizing text...')
            cleaned_text = ' '.join(text)
            self._text = nltk.word_tokenize(cleaned_text)


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

        self._word_trie.reset()

        # Create our own list of stop words, because otherwise there will be too many
        # stop words and the end result is that we just repeat the source data
        stop_words = {'the', 'a', 'an'}
        words_to_trie = []
        stop_words_to_save = []
        index = 0

        # Get first n words skipping stop words
        while len(words_to_trie) < self._order and index < num_words:
            if self._text[index] not in ".?!" and self._text[index] not in stop_words:
                words_to_trie.append(self._text[index])
            index += 1

        #Get the next word, and also record any possible stop words that come before it
        while len(words_to_trie) < self._order + 1 and index < num_words:
            if self._text[index] in stop_words:
                stop_words_to_save.append(self._text[index])
            else:
                if not self._text[index] in ".?!":
                    words_to_trie.append(self._text[index])
            index += 1

        # add first n words to trie
        if len(words_to_trie) == self._order + 1:
            self._word_trie.insert_words_and_increase_frequency(words_to_trie, ' '.join(stop_words_to_save))

        stop_words_to_save = []
        # go through remaining text and add to trie
        while index < num_words - self._order:
            while index < num_words - self._order and (self._text[index] in stop_words):
                stop_words_to_save.append(self._text[index])
                index += 1

            if not self._text[index] in ".?!":
                words_to_trie.pop(0)
                words_to_trie.append(self._text[index])
                self._word_trie.insert_words_and_increase_frequency(words_to_trie, ' '.join(stop_words_to_save))
                stop_words_to_save = []
            index += 1

        return '\nTRIE CREATED\n'




    def search_trie(self, words):
        """Searches the trie for the given list of words

        Args:
            words (array): word list to be located from the tree

        Returns:
            integer: the amount of times the word list has occurred in the source text
        """
        last_node = self._word_trie.traverse(words)
        if not last_node:
            return 0
        return last_node.frequency


    def generate_text(self, max_length, initial_words):
        """Generates text from the source file according to the Markov chain.

        Args:
            max_length (int): maximum amount of words to be generated
            initial_words (array): Optional. The first words that start the chain. Random words chosen if empty

        Returns:
            string: the generated text or an error message if fails
        """


        initial_words = self._word_trie.choose_initial_words(self._order)

        # Add the initial words to the text that will be returned
        generated_text = ' '.join(initial_words)


        base_words = initial_words[:]
        index = len(initial_words)

        while index < max_length:
            next_word, stop_words = self._word_trie.get_next_word(base_words)

            if not next_word:
                return generated_text

            if stop_words == '_NONE_':
                generated_text += ' ' + next_word
                base_words.pop(0)
                base_words.append(next_word)
            else:
                generated_text += ' ' + stop_words + ' ' + next_word
                base_words.pop(0)
                base_words.append(next_word)
            index += 1

        return generated_text

service = Service()

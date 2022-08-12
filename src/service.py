from random import choice
import re
from pathlib import Path
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from config import SOURCE_FILE_PATH
from trie import Trie


class Service():

    def __init__(self):
        self._text= []
        self._sentence_structures = []
        self._source_file = ''
        self._order = 2
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

    @order_sentence_structure.setter
    def order_sentence_structure(self, value):
        if value != self._order_sentence_structure:
            self._sentence_struct_trie.reset()
        self._order_sentence_structure = int(value)

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
            special_words = {"Mr.": "Mr", "Dr.": "Dr", "Mrs.": "Mrs", "Ms.": "Ms", "Prof.": "Prof", "e.g.": "eg", "i.e.": "ie"}
            previous_word = 'a'
            for line in f:
                line = line.strip()
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
                            text.append(special_words.get(cleaned_word))
                        else:
                            text.append(cleaned_word)


        cleaned_text = ' '.join(text)

        print('Performing sentence tokenization (this may take a few minutes)...')
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.tokenize(cleaned_text)
        count_sentences = len(sentences)
        print('Read total of '+ str(count_sentences) +' sentences')

        print('Tokenizing words and tagging parts of speech...')

        i = 0
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            words_pos = nltk.pos_tag(words)

            sentence_structure = []
            for word in words_pos:
                sentence_structure.append(word[1])
            self._sentence_structures.append(sentence_structure)

            words_to_remove = ".?!"
            for word_pos in words_pos:
                if not word_pos[0] in words_to_remove:
                    self._text.append((word_pos[0].lower(), word_pos[1]))

            # This is just to let the user know how the program is progressing
            i += 1
            if i % 1000 == 0:
                print('Tagged '+ str(i) + '/' + str(count_sentences))


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

        # Insert a word + the next n words into the trie
        # repeat for all words in source text file
        index = 0
        while index + self._order < num_words:
            words = []
            for i in range(self._order + 1):
                words.append(self._text[index + i])
            self._word_trie.insert_words_and_increase_frequency(words)
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

        # Here we select a structure to follow, e.g. pronoun - verb - preposition - article - adjective ...
        sentence_structure = []
        while len(sentence_structure) < 2 * max_length: #Change later? Now *2 to make sure we don't get index error when skipping '!?.'
            sentence_structure += choice(self._sentence_structures)
        
        # We need to select n initial words to start the chain
        if initial_words:
            if not self._word_trie.traverse(initial_words):
                return 'ERROR!!! COULD NOT GET INITIAL WORDS'
        else:
            try:
                initial_words = self._word_trie.choose_initial_words(self._order, sentence_structure)
            except:
                return 'SOMETHING WENT WRONG, TRY GENERATING TEXT AGAIN'

        # Add the initial words to the text that will be returned
        generated_text = ' '.join(initial_words)

        # Here we start the Markov process. We take n words and select the next word according to the probabilities of subsequent
        # words following the n words in the input text. Currently we also require that the word is has the same
        # part of speech (verb, noun, etc.) as required by the selected sentence structure
        base_words = initial_words
        amount_of_pos_to_skip = 0 # This is for skipping each ?!. in the sentence structure when getting the next word

        for i in range(self._order, max_length):
            # skipping .?! in the sentence structure. Every time there is a .!? in the sentence structure, we offset i by 1
            if sentence_structure[i + amount_of_pos_to_skip] in '.!?':
                generated_text += sentence_structure[i + amount_of_pos_to_skip]
                amount_of_pos_to_skip += 1

            # We get the next word according to the n previous words and require it to be of the form (verb, noun, etc.)
            # that is required in the sentence structure
            next_word = self._word_trie.get_next_word(base_words, sentence_structure[i + amount_of_pos_to_skip])

            # in case something goes wrong and we didn't get any more words
            if not next_word:
                return generated_text

            # word is added to generated text, and becomes part of the n words required to get the next word.
            # e.g. if we initially have the words: "the" "dog"   --> and we get the word "is",
            # the word "is" is added to the generated text, and the next word will be selected according to
            # the words: "dog" "is" --> "happy"
            generated_text += ' '+ next_word
            base_words.pop(0)
            base_words.append(next_word)

        return generated_text

service = Service()

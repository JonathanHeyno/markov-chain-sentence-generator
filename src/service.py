from pathlib import Path
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

        text = []
        with open(filepath, encoding = 'utf-8') as f:
            previous_word = 'a'
            for line in f:
                line = line.strip()
                words = line.split()
                for word in words:
                    text, previous_word = self._handle_special_characters(text, word, previous_word)
        print('Tokenizing text...')
        self._text = self.tokenize(text)
        self._source_file = filename
        return 'FILE READ'


    def _handle_special_characters(self, text, word, previous_word):
        chars_to_remove = "0123456789_\"+{}():;*&@$#[]-^-\\"
        special_words = {"Mr.": "Mr", "Dr.": "Dr", "Mrs.": "Mrs", "Ms.": "Ms", "Prof.": "Prof", "E.g.": "Eg", "I.e.": "Ie", "etc.": "etc", "i.e.": "ie", "e.g.": "eg"}
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
                if len(cleaned_word) > 1 and cleaned_word[-2] in "!.,?":
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


        return text, previous_word

    def tokenize(self, text):
        """tokenizes input text

        Args:
            text (array): an array of stext

        Returns:
            array: an array of text that is tokenized
        """
        tokenized_text = []
        for word in text:
            word_length = len(word)
            punct_at_end = ''
            second_part = ''
            if word_length >= 2 and word[-1] in [".", ",", "?", "!"]:
                punct_at_end = word[-1]
                word = word[:-1]
            if word_length >= 2 and word[-1] in ["'"]:
                second_part = word[-1:]
                word = word[:-1]
            if word_length >= 3 and word[-2:] in ["'s", "'d", "'v"]:
                second_part = word[-2:]
                word = word[:-2]
            if word_length >= 4 and word[-3:] in [ "n't", "'ve", "'ll", "'re"]:
                second_part = word[-3:]
                word = word[:-3]

            tokenized_text.append(word)
            if second_part:
                tokenized_text.append(second_part)
            if punct_at_end:
                tokenized_text.append(punct_at_end)
        return tokenized_text

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
        stop_words_to_save = []
        words_to_trie = []
        index = 0

        # We mark down if a word is followed or preceded by .,?!
        followed_by = ''
        preceded_by = ''

        # Get first n words skipping stop words
        while len(words_to_trie) < self._order and index < num_words:
            if self._text[index] not in ".,?!" and self._text[index] not in stop_words:
                words_to_trie.append(self._text[index])
            index += 1

        # Get the next word, and also record any possible stop words, and .?!
        # that come before it. We do not need to worry about the order of .?!
        # and stop words, since our stop words are only 'a', 'an', 'the'
        # so any .?! will typically come before them
        while len(words_to_trie) < self._order + 1 and index < num_words:
            if self._text[index] in stop_words:
                stop_words_to_save.append(self._text[index])
            else:
                if self._text[index] in ".,?!":
                    preceded_by += self._text[index]
                else:
                    words_to_trie.append(self._text[index])
            index += 1

        # Check if there are any .?! after the selected word
        # While loop because we might have '!?', '...', etc.
        i = 0
        while index + i < num_words:
            if not self._text[index + i] in ".,?!":
                break
            followed_by += self._text[index + i]
            i += 1

        # add first n words to trie
        if len(words_to_trie) == self._order + 1:
            self._word_trie.insert_words_and_increase_frequency(words_to_trie, ' '.join(stop_words_to_save), preceded_by, followed_by)


        stop_words_to_save = []
        preceded_by = ''
        followed_by = ''

        # go through remaining text and add to trie
        while index < num_words:

            if self._text[index] in ".,?!":
                preceded_by += self._text[index]

            elif self._text[index] in stop_words:
                stop_words_to_save.append(self._text[index])

            else:
                words_to_trie.pop(0)
                words_to_trie.append(self._text[index])
                i = 1
                # while loop to see if a word is followed by .,?!
                while index + i < num_words:
                    if not self._text[index + i] in ".,?!":
                        break
                    followed_by += self._text[index + i]
                    i += 1
                self._word_trie.insert_words_and_increase_frequency(words_to_trie, ' '.join(stop_words_to_save), preceded_by, followed_by)
                stop_words_to_save = []
                preceded_by = ''
                followed_by = ''
            index += 1

        return 'TRIE CREATED\n'



    def generate_text(self, max_length):
        """Generates text from the source file according to the Markov chain.

        Args:
            max_length (int): maximum amount of words to be generated
            initial_words (array): Optional. The first words that start the chain. Random words chosen if empty

        Returns:
            string: the generated text or an error message if fails
        """
        initial_words, initial_nodes = self._word_trie.choose_initial_words(self._order)

        words = initial_words[:]
        nodes = initial_nodes[:]


        base_words = initial_words[:]
        index = len(initial_words)

        while index < max_length:
            next_word, next_node = self._word_trie.get_next_word(base_words)

            if not next_word:
                break

            words.append(next_word)
            nodes.append(next_node)
            base_words.pop(0)
            base_words.append(next_word)
            index += 1

        generated_text = self.post_process(words, nodes)

        return generated_text


    def post_process(self, words, nodes):
        """Post process text to fix grammar and insert punctuations and stop words

        Args:
            words (array): an array of tokenized words
            nodes (array): the corresponding nodes of the words

        Returns:
            String: the processed text
        """
        text = []
        text.append(words[0])
        num_words = len(words)
        index = 1
        while index < self._order:
            text.append(words[index])
            index += 1

        while index < num_words:
            previous_word_followed_by = nodes[index-1].followed_by
            preceded_by = nodes[index].preceded_by
            punctuation = self.check_if_must_put_punctuation(previous_word_followed_by, preceded_by)
            if punctuation:
                text.append(punctuation)
            stop_words = self.check_if_must_put_stop_word(nodes[index])
            if stop_words:
                text.append(stop_words)
            text.append(words[index])
            index += 1

        return self.fix_words(text)

    def check_if_must_put_punctuation(self, previous_word_followed_by, preceded_by):
        """Determines if a punctuation like .,?! needs to be placed between two words

        Args:
            previous_word_followed_by (array): an array of the different punctuations
            that followed the previous word
            preceded_by (array): an array of the different punctuations that preceded the given word

        Returns:
            String: a punctuation that should come between the two words, or an empty string
        """
        # If the previous word is always followed by .,?! and the next word is always preceded by .,?!
        # we assume a .,?! must be placed between these two words, default is '.'
        punct = ''
        if not '_NONE_' in previous_word_followed_by and not '_NONE_' in preceded_by:
            punct = '.'
            for char in previous_word_followed_by:
                if char in preceded_by:
                    punct = char
        return punct

    def check_if_must_put_stop_word(self, node):
        """Determines if a stop word like 'a' or 'the' needs to be placed before the word

        Args:
            node: the node of the word

        Returns:
            String: the stop word that comes before this word or an empty string
        """
        stop_words = list(node.stop_words.keys())
        for stop_word in stop_words:
            if stop_word != '_NONE_':
                return stop_word
        return ''
        
    def fix_words(self, text):
        """Concatenates some tokenizations and capitalizes some words.

        Args:
            text (array): the tokenized text

        Returns:
            String: the fixed text
        """
        fixed_text = text[0].capitalize()
        index = 1
        endings_to_concatenate = ["'", "'s", "'d", "'v", "n't", "'ll", "'ve", "'re", ".", ",", "?", "!"]
        special_words = {"mr": "Mr.", "dr": "Dr.", "mrs": "Mrs.", "ms": "Ms.", "prof": "Prof.", "eg": "e.g.", "ie.": "i.e.", "etc": "etc."}
        previous_word = text[0].capitalize()
        while index < len(text):
            word = text[index]
            if word in special_words:
                word = special_words.get(word)
            if previous_word in ".?!" or word =='i':
                word = word.capitalize()
            if word in endings_to_concatenate:
                fixed_text += word
            else:
                fixed_text += ' ' + word
            previous_word = word
            index += 1
        return fixed_text

service = Service()

import unittest
from service import Service

class TestService(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.service.read_source_file('text_for_pytest.txt')


    def test_read_source_file(self):
        self.assertTrue(self.service.source_file)
        self.assertTrue(self.service._text)

    def test_read_inexisting_source_file_fails(self):
        self.assertGreater(len(self.service.read_source_file('nofile.txt')), 22)

    def test_frequency_of_words_correct_in_trie(self):
        self.service.create_trie_and_count_frequencies()
        words = ['and', 'god', 'said']
        self.assertEqual(self.service.search_trie(words), 10)

    def test_error_when_markov_order_greater_than_word_count(self):
        self.service.order=30000000
        message = self.service.create_trie_and_count_frequencies()
        self.assertEqual(message, '\nORDER OF MARKOV CHAIN LARGER THAN WORD COUNT IN SOURCE FILE\n' )

    def test_search_trie_for_words_that_do_not_exist(self):
        self.service.create_trie_and_count_frequencies()
        words = ['and', 'myyyy', 'bbb']
        self.assertEqual(self.service.search_trie(words), 0)

    def test_can_reset_markov_chain_order(self):
        self.service.create_trie_and_count_frequencies()
        self.service.order=3
        self.assertAlmostEqual(self.service.order, 3)
        words = ['and', 'god', 'said', 'let']
        self.assertEqual(self.service.search_trie(words), 0)

    def test_can_generate_txt(self):
        self.service.create_trie_and_count_frequencies()
        generated_text = self.service.generate_text(200, [])
        self.assertGreater(len(generated_text), 2)

    def test_can_generate_txt_with_given_initial_words(self):
        self.service.create_trie_and_count_frequencies()
        generated_text = self.service.generate_text(200, ['earth', 'after'])
        self.assertGreater(len(generated_text), 12)

    def test_fail_to_generate_text_with_faulty_initial_words(self):
        self.service.create_trie_and_count_frequencies()
        generated_text = self.service.generate_text(200, ['aaaa', 'bbbbb'])
        self.assertEqual(generated_text, 'ERROR!!! COULD NOT GET INITIAL WORDS')

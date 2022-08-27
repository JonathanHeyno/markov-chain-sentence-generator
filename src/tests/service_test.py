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

    def test_error_when_markov_order_greater_than_word_count(self):
        self.service.order=30000000
        message = self.service.create_trie_and_count_frequencies()
        self.assertEqual(message, '\nORDER OF MARKOV CHAIN LARGER THAN WORD COUNT IN SOURCE FILE\n' )

    def test_can_reset_markov_chain_order(self):
        self.service.create_trie_and_count_frequencies()
        self.service.order=2
        self.service.create_trie_and_count_frequencies()
        self.assertEqual(self.service.order, 2)

    def test_can_generate_txt(self):
        self.service.create_trie_and_count_frequencies()
        generated_text = self.service.generate_text(200)
        self.assertGreater(len(generated_text), 2)

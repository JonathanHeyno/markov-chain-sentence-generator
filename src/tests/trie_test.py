import unittest
from trie import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        text = ['I', 'want', 'candy']
        stop_words = 'a'
        preceded_by = ''
        followed_by = '.'
        self.trie = Trie()
        self.trie.order = 2
        self.trie.insert_words_and_increase_frequency(text, stop_words, preceded_by, followed_by)

    def test_can_change_order(self):
        self.trie.order = 4
        self.assertEqual(self.trie.order, 4)

    def test_can_insert_words(self):
        text = ['I', 'want', 'cat']
        stop_words = 'a'
        preceded_by = ''
        followed_by = '.'
        self.trie.insert_words_and_increase_frequency(text, stop_words, preceded_by, followed_by)
        node = self.trie.traverse(text)
        self.assertTrue(node)

    def test_can_increase_frequency(self):
        text = ['I', 'want', 'candy']
        stop_words = 'a'
        preceded_by = ''
        followed_by = '.'
        self.trie.insert_words_and_increase_frequency(text, stop_words, preceded_by, followed_by)
        node = self.trie.traverse(text)
        self.assertEqual(node.frequency, 2)

    def test_can_traverse_trie(self):
        text = ['I', 'want', 'candy']
        node = self.trie.traverse(text)
        self.assertTrue(node)

    def test_traversing_trie_with_no_words_returns_root(self):
        text = []
        node = self.trie.traverse(text)
        self.assertEqual(node, self.trie._root)

    def test_traversing_trie_with_incorrect_words_fails(self):
        text = ['I', 'want', 'wall']
        node = self.trie.traverse(text)
        self.assertFalse(node)

    def test_can_choose_initial_words(self):
        text = ['I', 'want', 'cat']
        stop_words = 'a'
        preceded_by = ''
        followed_by = '.'
        self.trie.insert_words_and_increase_frequency(text, stop_words, preceded_by, followed_by)
        words, nodes = self.trie.choose_initial_words(2)
        self.assertEqual(len(words), 2)
        self.assertEqual(len(nodes), 2)

    def test_choose_initial_words_fails_if_order_too_small(self):
        text = ['I', 'want', 'cat']
        stop_words = 'a'
        preceded_by = ''
        followed_by = '.'
        self.trie.insert_words_and_increase_frequency(text, stop_words, preceded_by, followed_by)
        words, nodes = self.trie.choose_initial_words(4)
        self.assertFalse(words)

    def test_can_get_next_word(self):
        word, node = self.trie.get_next_word(['I', 'want'])
        self.assertEqual(word, 'candy')
        self.assertTrue(node)

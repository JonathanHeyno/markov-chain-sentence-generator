import unittest
from node import Node

class TestNode(unittest.TestCase):
    def setUp(self):
        self.node = Node()

    def test_can_insert_child(self):
        node = self.node.insert_and_return_child_node('child')
        self.assertTrue(node)

    def test_can_increase_frequency(self):
        self.node.increase_word_frequency()
        self.assertTrue(self.node.frequency, 1)

    def test_can_get_child(self):
        node = self.node.insert_and_return_child_node('child')
        self.assertEqual(self.node.get_child_node('child'), node)

    def test_get_child_that_does_not_exist_fails(self):
        node = self.node.insert_and_return_child_node('child')
        self.assertFalse(self.node.get_child_node('child2'), node)

    def test_can_increase_stop_word_frequency(self):
        self.node.increase_stop_word_frequency('the')
        is_in_list = 'the' in list(self.node.stop_words.keys())
        self.assertTrue(is_in_list)

    def test_can_increase_preceded_by_frequency(self):
        self.node.increase_preceded_by_frequency('.')
        is_in_list = '.' in list(self.node.preceded_by.keys())
        self.assertTrue(is_in_list)

    def test_can_increase_followed_by_frequency(self):
        self.node.increase_followed_by_frequency('.')
        is_in_list = '.' in list(self.node.followed_by.keys())
        self.assertTrue(is_in_list)

    def test_increase_stop_word_frequency_when_no_stop_word(self):
        self.node.increase_stop_word_frequency('')
        is_in_list = '_NONE_' in list(self.node.stop_words.keys())
        self.assertTrue(is_in_list)

    def test_increase_preceded_by_frequency_when_no_preceded_by(self):
        self.node.increase_preceded_by_frequency('')
        is_in_list = '_NONE_' in list(self.node.preceded_by.keys())
        self.assertTrue(is_in_list)

    def test_can_increase_followed_by_frequency_when_no_followed_by(self):
        self.node.increase_followed_by_frequency('')
        is_in_list = '_NONE_' in list(self.node.followed_by.keys())
        self.assertTrue(is_in_list)

    def test_can_choose_a_child(self):
        node = self.node.insert_and_return_child_node('child')
        word, node2 = self.node.choose_any_child()
        self.assertEqual(word, 'child')

    def test_can_choose_a_child_fails_when_no_children(self):
        word, node2 = self.node.choose_any_child()
        self.assertFalse(word)

    def test_can_select_next_word(self):
        node = self.node.insert_and_return_child_node('child')
        node.increase_word_frequency()
        word, node2 = self.node.select_next_word()
        self.assertEqual(word, 'child')

    def test_select_next_word_fails_when_no_words(self):
        word, node2 = self.node.select_next_word()
        self.assertFalse(word)

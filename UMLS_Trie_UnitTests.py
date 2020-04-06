import unittest
import UMLS_Trie as trie
import replace_string as tsr


class TestTrieCreation(unittest.TestCase):

    # Create the test information for later use
    def setUp(self):
        self.test_trie = trie.trie()
        self.test_data_map = {"heart": "S1", "attack": "S2", "heart attack": "S3", "heart attack complication": "S4",
                              "other symptoms": "S5", "other": "S6", "my attack": "S7"}

    # test to make sure trie object created
    def test_trie_created(self):
        self.assertIsInstance(self.test_trie, trie.trie)

    # test to check that trie rejects non-string insertions
    def test_non_string_insertion(self):
        with self.assertRaises(TypeError):
            self.test_trie.insert_string(2323, " ", "code")

    # tests to ensure that the insertion worked
    def test_insert_data(self):
        # inserting the data into the trie
        for key, value in self.test_data_map.items():
            self.test_trie.insert_string(key, " ", value)

        self.assertEqual(self.test_trie.root_node.umls_values, {"heart": "S1", "attack": "S2", "other": "S6", "my": "\0"})
        self.assertEqual(len(self.test_trie.root_node.next_node), 3)


class TestTrieCodes(unittest.TestCase):

    # Create the test information for later use
    def setUp(self):
        self.test_trie = trie.trie()
        self.test_data_map = {"I": "S1", "I love": "S2", "I love you mom": "S3", "love you": "S4"}
        for key, value in self.test_data_map.items():
            self.test_trie.insert_string(key, " ", value)

    def test_no_matches(self):
        self.assertEqual(self.test_trie.get_codes("No matches to be found", " "), ([]), "no matches")

    def test_simple_match(self):
        codes = self.test_trie.get_codes("I love", " ")
        self.assertEqual(len(codes), 1, "length doesn't match")
        self.assertEqual(codes[0], (0, 1, "S2", "I love"), "match incorrect")

    def test_overlapping_matches(self):
        codes = self.test_trie.get_codes("I love you", " ")
        self.assertEqual(len(codes), 2, "length doesn't match")
        self.assertEqual(codes[0], (0, 1, "S2", "I love"), "first match incorrect")
        self.assertEqual(codes[1], (1, 2, "S4", "love you"), "second match incorrect")



class TestReplace(unittest.TestCase):

    # Create the test information for later use
    def setUp(self):
        self.test_trie = trie.trie()
        self.test_data_map = {"I": "S1", "I love": "S2", "I love you mom": "S3", "love you": "S4"}
        for key, value in self.test_data_map.items():
            self.test_trie.insert_string(key, " ", value)

    # test the ability to replace
    def test_simple_replace(self):
        returned = tsr.replace_string("I love", [(0, 1, 'S2', 'I love')])
        self.assertEqual(returned, "S2")

    # replacement test with multiple in a row
    def test_overlapping_replace(self):
        self.assertEqual("S2 you", tsr.replace_string("I love you", [(0, 1, 'S2', 'I love'), (1, 2, 'S4', 'love you')]))

    def test_multiple_replace(self):
        test_string = "I love my mom so I said: I love you mom"
        codes = self.test_trie.get_codes(test_string, " ")
        returned = tsr.replace_string(test_string, codes)
        self.assertEqual("S2 my mom so S1 said: S3", returned)

    def test_code_start_index_out_of_range(self):
        codes = [(0, 1, "S2", "I love"), (3, 4, "S6", "another replace")]
        returned = tsr.replace_string("I love you", codes)
        self.assertEqual("S2 you", returned)

    def test_code_end_index_out_of_range(self):
        codes = [(0, 1, "S2", "I love"), (2, 4, "S6", "another replace")]
        returned = tsr.replace_string("I love you", codes)
        self.assertEqual("S2 S6", returned)

class TestTrieNode(unittest.TestCase):

    # Check to see if node properly created with no values in maps
    def test_create_node(self):
        node = trie.trie_node()
        self.assertIsInstance(node, trie.trie_node)
        self.assertEqual(0, len(node.umls_values))
        self.assertEqual(0, len(node.next_node))

    # insert a code and a string with no deliminations
    # checks to see if code for the string "test" is code1 in the map
    # trying to get the next_node directly from the map should raise an error because no next_node is inserted
    def test_insert_string_no_spaces(self):
        node = trie.trie_node()
        node.insertValues(["test"], "code1")
        self.assertEqual(node.umls_values["test"], "code1")
        with self.assertRaises(KeyError):
            node.next_node["test"]

    # inserts an already split string with two words
    # checks that the inserted value for the first node's UMLS_values is the null character
    # checks that the inserted value for the second node's UMLS_values is the actual code
    def test_insert_string_spaced(self):
        node = trie.trie_node()
        node.insertValues(["test", "case"], "code1")
        self.assertEqual(node.umls_values["test"], "\0")
        self.assertIsInstance(node.next_node["test"], trie.trie_node)
        nested_node = node.next_node["test"]
        self.assertEqual(nested_node.umls_values["case"], "code1")
        self.assertEqual(0, len(nested_node.next_node))

    # tests the method of getting a nested node from a trie_node
    # tests that get_node returns type trie_node
    # tests that the values from the returned node are correct
    # tests that a node who's key isn't present in both maps returns none
    def test_get_node(self):
        node = trie.trie_node()
        node.insertValues(["test", "case"], "code1")
        nested_node = node.getNode("test")
        self.assertIsInstance(nested_node, trie.trie_node)
        self.assertEqual(nested_node.umls_values["case"], "code1")
        self.assertEqual(node.getNode("failure"), None)

    # tests if the code can be retrieved from a node
    def test_get_code(self):
        node = trie.trie_node()
        node.insertValues(['hello'], 'code')
        self.assertEqual(node.getUMLSCode('hello'), 'code')


if __name__ == "__main__":
    unittest.main()


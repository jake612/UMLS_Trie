from UMLS_Trie import trie
from replace_string import replace_string


if __name__ == '__main__':
    # Insert the keys
    test_trie = trie()
    test_data_map = {"I": "S1", "I love": "S2", "I love you mom": "S3", "love you": "S4"}
    for key, value in test_data_map.items():
        test_trie.insert_string(key, " ", value)

    # Get strings with instances replaced by keys
    test_strings = ['I love you', 'I love you mom', 'I think I love her']
    new_strings = []
    for string in test_strings:
        codes = test_trie.get_codes(string, " ")
        new_strings.append(replace_string(string, codes))

    # print results
    for string in new_strings:
        print(string)

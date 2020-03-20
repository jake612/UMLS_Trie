# UMLS Trie: Maximal Pattern Replacement
This code was written to solve a problem I faced during my research. Given a list of UMLS codes for different medical terms, I needed to replace the term with a given code in a Reddit comment string. The replacement has to be maximal, i.e. we don't want to replace "heart attack" with the individual codes for "heart" and "attack" but the code for the term "heart attack" if it is in the trie. The trie class has methods for loading the key-value pairs and replacing substrings with the loaded key-value pairs.

Ex: "I had a heart attack yesterday" being replaced by the string "I had a S1 yesterday", with S1 being the given code for "heart attack"

# Methods
**insert_string:** Method for loading a string with an associated code into a trie structure.

 - Arguments
	 - string: the string to be loaded
		 - Must be type string
		 - ex: "heart attack"
	 - delimiter: the delimiter for splitting the string into multiple parts
		 - ex: " " to split "heart attack" into ["heart", "attack"]
	 - umls_code: the code to associate with the given string
		 - ex: "S1" associated with "heart attack"

return value: True if inserted, false if already in trie

**replace_string:** Method for replacing substrings within a string that are associated with loaded codes

 - Arguments
	 - string: the string you want to replace substrings within
		 - ex: "I had a heart attack"
	 - delimiter: a delimiter for splitting the values to search for maximal substring patterns
		 - ex: " " with "I had a heart attack" would split it into ["I", "had", "a", "heart", "attack"]. The algorithm would then focus on replacements based on each string in the list.
		
return value: A string with the substrings replaced by loaded codes, if any
	ex: "I had a S1" based on the above example

**print_vals:** A depth-first printing of the string-code pairs in the trie. Pretty rough, I just wrote for personal debugging

# Usage Example

Loading strings and codes into the trie

    import UMLS_Trie as trie
    
    test_trie = trie.trie()
    key_pairs = {"heart": "S1", "attack": "S2", "heart attack": "S3"}
    for key, value in key_pairs.items():
	    test_trie.insert_string(key, " ", value)

Getting a list of replaced strings

 

    strings= ["I had a heart attack",
			  "heart problems",
			  "massive attack"]
	replaced_strings = []
	for string in strings:
		new_string = test_trie.replace_string(string, " ")
		replaced_strings.append(new_string)


# UMLS Trie: Maximal Pattern Codes
This code was written to solve a problem I faced during my research. Given a list of UMLS codes for different medical terms, I needed to replace the term with a given code in a Reddit comment string. The replacement has to be maximal, i.e. we don't want to replace "heart attack" with the individual codes for "heart" and "attack" but the code for the term "heart attack" if it is in the trie. The trie class has methods for loading the key-value pairs and getting codes with the loaded key-value pairs.


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

**get_codes:** Method for retrieving substrings that match a given string in the trie. 

Each code is a tuple in the following format: (starting_index, finishing_index, code, associated_string). So, if the string "blue bird" was inserted into the trie with code "S1" and get_codes was called on the string "I saw a blue bird today", the returned list of codes would be [(3, 4, "S1", "blue bird")]. The returned codes are maximal. If "blue" was also a string in the trie with an associated code, it wouldn't be returned as a code in the previous example, as "blue bird" is the maximal pattern.

Codes can also be returned if they overlap. If "I love" and "love you" were loaded into the trie and get_codes was called on "I love you",
[(0, 1, "S1", "I love"), (1, 2, "S2", "love you")] would be returned.

 - Arguments
	 - string: the string to return codes from
		 - Must be type string
		 - ex: "heart attack"
	 - delimiter: the delimiter for splitting the string into multiple parts
		 - ex: " " to split "heart attack" into ["heart", "attack"]

return value: A list of codes found within the string.
		
**print_vals:** A depth-first printing of the string-code pairs in the trie. Pretty rough, I just wrote for personal debugging.

# Replace String
replace_string is a function built to leverage codes returned from the get_codes method of the trie.
Given a string and its associated codes from get_codes, it replaces substrings with their umls_codes.
For example, given "I saw a blue bird today" and [(3, 4, "S1", "blue bird")], it would return string "I saw a S1 today". It's important to note that if two substrings overlap like in the "I love you" example, only the first substring will be replaced by its umls_code (ie "S1 you").

 - Arguments
	 - string: the string to replace substrings with their umls_code
		 - Must be type string
		 - ex: "I love you"
	 - codes: a list of codes in the format from UMLS_Trie.get_codes
		 - ex: [(start_index, end_index, code, string), (start_index, end_index, code, string)]

return value: string with its substrings replaced by their umls codes.

# Usage Example

Found in example_trie_replace.py

# Explore Trie
The explore trie script allows a user to test out a pickled UMLS_Trie in the command line.
It's a good way to test replace_string and get_codes.

- Using the explore_trie.py script
    - The first command line argument is always the file name of the pickled trie.
    - No further arguments:
       loads a cli interactive script where a users 
    can continuously enter sentences. The script will print out the sentence with its
    maximal patterns replaced by their code from the loaded pickled UMLS_Trie. Type "exit" to exit the program loop.
        - ex: python explore_trie.py pickle_trie.p
    - The "-s" argument: If there is an "-s" switch after the pickle file argument and a sentence argument after that,
    the script will run get_codes and replace_string on the supplied sentence much like in the case of no argument.
        - python explore_trie.py pickle_trie.p -s "Test replacing me"



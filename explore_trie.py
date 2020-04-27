import pickle
import sys
from replace_string import replace_string

def continuous_test(trie):
    while True:
        string = input("Enter a string to be replaced or exit to exit this program:\n")
        if string == "exit":
            break
        else:
            codes = trie.get_codes(string, " ")
            print("Output:")
            print(replace_string(string, codes))

if __name__ == "__main__":

    try:
        # Load Trie from argument
        with open(sys.argv[1], "rb") as file:
            trie = pickle.load(file)
    except:
        print("Error loading file")
        exit()

    print("Loaded trie file: " + sys.argv[1])

    if len(sys.argv) == 4 and sys.argv[2] == "-s":
        codes = trie.get_codes(sys.argv[3], " ")
        print("Output:")
        print(replace_string(sys.argv[3], codes))
    else:
        continuous_test(trie)



# Class holds root node and allows interaction with trie structure
class trie:
    def __init__(self):
        self.root_node = trie_node()

    # Returns true if new string added, false if already existed
    # TypeError raised if not string, ValueError raised if string is just ""
    def insert_string(self, string, delimiter, umls_code):
        if not isinstance(string, str):
            raise TypeError
        values = string.split(delimiter)
        if len(values) == 0:
            raise ValueError
        return self.root_node.insertValues(values, umls_code)

    def get_codes(self, string, delimiter):
        return_codes = []

        vals = string.split(delimiter)
        vals = list(filter(lambda a: a != delimiter, vals)) # filters out additional whitespaces

        for i in range(len(vals)):
            final_code = None
            end_index = 0
            string_vals = []
            past_nils = 0

            offset = i
            node = self.root_node
            while offset < len(vals) and node is not None:
                umls_code = node.getUMLSCode(vals[offset])
                if umls_code is None:
                    break
                else:
                    if umls_code != "\0":
                        final_code = umls_code
                        end_index = offset
                        past_nils = 0
                    else:
                        past_nils += 1
                    node = node.getNode(vals[offset])
                string_vals.append(vals[offset])
                offset += 1

            if final_code is not None and (len(return_codes) == 0 or end_index > return_codes[-1][1]):
                return_codes.append((i, end_index, final_code, " ".join(string_vals[:-past_nils or None])))

        return return_codes

    def print_vals(self):
        self.root_node.print_vals()


class trie_node:
    def __init__(self):
        # umls_values dictionary holds key (string) and UMLS Code
        self.umls_values = {}

        # dictionary holds key (string) and reference to next possible string value
        self.next_node = {}

    def insertValues(self, values, umls_code):
        if values[0] in self.umls_values:
            if len(values) == 1:
                # if the value is placeholder, replace it with new code
                if self.umls_values[values[0]] is '\0':
                    self.umls_values[values[0]] = umls_code
                    return True
                elif values[0] not in self.next_node:
                    return False
            else:
                if values[0] in self.next_node:
                    return self.next_node[values[0]].insertValues(values[1:], umls_code)
                else:
                    self.next_node[values[0]] = trie_node()
                    return self.next_node[values[0]].insertValues(values[1:], umls_code)
        else:
            if len(values) == 1:
                self.umls_values[values[0]] = umls_code
                return True
            else:
                # if there are more values left in the given value list, create a new node
                new_trie_node = trie_node()
                # Set the value to a placeholder null character to indicate that this is not an ending value
                self.umls_values[values[0]] = '\0'
                self.next_node[values[0]] = new_trie_node
                return new_trie_node.insertValues(values[1:], umls_code)

    def getNode(self, value):
        if value in self.umls_values and value in self.next_node:
            return self.next_node[value]
        else:
            return None

    def getUMLSCode(self, val):
        if val in self.umls_values:
            return self.umls_values[val]
        else:
            return None

    def print_vals(self):
        for string in self.umls_values.keys():
            if string in self.next_node and self.next_node[string] is not None:
                self.next_node[string].print_vals()
            print(string + ": " + self.umls_values[string])



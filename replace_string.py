def replace_string(string, codes):
    if len(codes) == 0:
        return string
    vals = string.split(" ")
    vals = list(filter(lambda a: a != " ", vals))  # filters out additional whitespaces

    return_string = ""
    current_code = codes[0]

    i = 0
    while i < len(vals):
        if current_code is not None and i == current_code[0]:
            return_string += current_code[2] + " "
            i += current_code[1] - current_code[0] + 1
            codes = codes[1:]
            if len(codes) == 0:
                current_code = None
            else:
                current_code = codes[0]
        else:
            return_string += vals[i] + " "
            i += 1

    return return_string[:-1]

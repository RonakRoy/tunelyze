key_mapping = ['C', 'C#/D♭', 'D', 'D#/E♭', 'E', 'F', 'F#/G♭', 'G', 'G#/A♭', 'A', 'A#/B♭', 'B']

def get_english_list(l):
    length = len(l)

    if length == 1:
        return l[0]

    elif length == 2:
        return "{} and {}".format(l[0], l[1])

    else:
        output = ""

        for i in range(length - 1):
            output += "{}, ".format(l[i])
        output += "and {}".format(l[length-1])

        return output

def get_delimited_list(l, delim):
    output = ""
    length = len(l)
    for i in range(length - 1):
        output += "{}{}".format(l[i], delim)
    output += "{}".format(l[length-1])

    return output

def get_alpha_key(int_key):
    return key_mapping[int_key]
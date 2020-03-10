key_mapping = ['C', 'C#/D♭', 'D', 'D#/E♭', 'E', 'F', 'F#/G♭', 'G', 'G#/A♭', 'A', 'A#/B♭', 'B']

def get_english_list(l):
    length = len(l)

    if length == 0:
        return "none"

    elif length == 1:
        return l[0]

    elif length == 2:
        return "{} and {}".format(l[0], l[1])

    else:
        output = ""

        for i in range(length - 1):
            output += "{}, ".format(l[i])
        output += "and {}".format(l[length-1])

        return output

def get_delimited_list(l, delimiter):
    output = ""
    length = len(l)
    for i in range(length - 1):
        output += "{}{}".format(l[i], delimiter)
    output += "{}".format(l[length-1])

    return output

def get_alpha_key(int_key):
    return key_mapping[int_key]

def input_boolean(prompt):
    while True:
        result = input(prompt + " (enter \'y\' or \'n\'): ")
        if result == 'y':
            return True
        elif result == 'n':
            return False
        else:
            print("Sorry, but that input is invalid.")

def input_sublist(prompt, l):
    if len(l) == 0:
        return []

    for i, e in enumerate(l):
        print("  [{}] {}".format(i, e))
    
    while True:
        raw_input = input(prompt + " (enter a list of numbers from 0 to {}, separated by spaces): ".format(len(l)-1))
        inputs = raw_input.split()
        selections = []

        try:
            for e in inputs:
                selections.append(l[int(e)])        
            return selections
        except:
            print("Sorry, but that input is invalid.")
            break
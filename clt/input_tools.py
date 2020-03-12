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
                i = int(e)
                if i >= len(l):
                    raise

                selections.append(l[i])        
            return selections
        except:
            print("Sorry, but that input is invalid.")
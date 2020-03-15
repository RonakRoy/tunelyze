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
        rawinput = input(prompt + " (enter a comma-separated list of numbers and ranges (ex: \'1,3,5-10\'), with valid indecies and range endpoint between 0 to {}, inclusive): ".format(len(l)-1))
        inputs = rawinput.strip().split(',')
        if inputs == ['']:
            return []

        selections = []

        try:
            for e in inputs:
                if '-' in e:
                    bounds = e.split('-')
                    if len(bounds) != 2:
                        raise

                    low = int(bounds[0])
                    high = int(bounds[1])

                    if not low in range(0,len(l)) or not high in range(0,len(l)) or low > high:
                        raise

                    for i in range(low, high+1):
                        selections.append(l[i])
                else:
                    i = int(e)
                    if i >= len(l):
                        raise

                    selections.append(l[i])        
            return selections
        except:
            print("Sorry, but that input is invalid.")
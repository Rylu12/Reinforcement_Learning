import sys

def read_map(filename):
    """Reads the text file race track map"""
    with open( filename, 'r') as f:
        world_data = [x for x in f.readlines()]

    f.closed


    map = []
    for i,line in enumerate(world_data):
        #Skip the first line
        if i > 0:

            line = line.strip()

            #Skip loop if line is blank
            if line == "":
                continue

           #Save all char in line
            map.append([x for x in line])
    return map


def print_map(map):
    """Prints the race track map for animation purposes"""

    text=''
    print()
    for line in map:
        for cell in line:
            #Collect each character in text file row
            text += cell
        text = text +'\n'

    sys.stdout.write('\r' + text)
    sys.stdout.flush()

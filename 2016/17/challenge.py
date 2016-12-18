from hashlib import md5
from itertools import count

PASSCODE = 'gdjjyniy'


def is_open(c):
    return c in 'bcdef'


def generate_options((x, y, path)):
    hash = md5(PASSCODE + path).hexdigest()
    if y > 0 and is_open(hash[0]):
        yield x, y-1, 'U'
    if y < 3 and is_open(hash[1]):
        yield x, y+1, 'D'
    if x > 0 and is_open(hash[2]):
        yield x-1, y, 'L'
    if x < 3 and is_open(hash[3]):
        yield x+1, y, 'R'


def find_paths():
    states = {(0, 0, ''),}
    shortest_path = None
    while states:
        new_states = set()
        for state in states:
            for new_x, new_y, move in generate_options(state):
                if (new_x, new_y) == (3, 3):
                    longest_path = state[2] + move
                    if shortest_path is None:
                        shortest_path = longest_path
                else:
                    new_states.add((new_x, new_y, state[2] + move))
        states = new_states
    return shortest_path, longest_path

shortest_path, longest_path = find_paths()

print "Part One:", shortest_path
print "Part Two:", len(longest_path)

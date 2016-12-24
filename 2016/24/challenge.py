from collections import defaultdict, namedtuple
from itertools import chain
from Queue import PriorityQueue

MAP = defaultdict(bool)
NODES = defaultdict(frozenset)
TARGET_NODES = set()
START = None

State = namedtuple('State', 'current_loc steps_so_far left_to_visit')


def priority(state):
    return state.steps_so_far + min(abs(x - state.current_loc[0]) + abs(y - state.current_loc[1]) for x, y in TARGET_NODES)


def generate_options(((x, y), steps_so_far, left_to_visit)):
    steps_so_far += 1
    if MAP[x - 1, y] and BEST_PATHS[x - 1, y][left_to_visit] > steps_so_far:
        yield x - 1, y
    if MAP[x + 1, y] and BEST_PATHS[x + 1, y][left_to_visit] > steps_so_far:
        yield x + 1, y
    if MAP[x, y - 1] and BEST_PATHS[x, y - 1][left_to_visit] > steps_so_far:
        yield x, y - 1
    if MAP[x, y + 1] and BEST_PATHS[x, y + 1][left_to_visit] > steps_so_far:
        yield x, y + 1


def visit(new_loc, last_state):
    left_to_visit = last_state.left_to_visit - NODES[new_loc]
    new_state = State(new_loc, last_state.steps_so_far + 1, left_to_visit)
    return priority(new_state), new_state


with open('input.txt') as input_file:
    for y, line in enumerate(input_file):
        for x, c in enumerate(line):
            MAP[x, y] = c != '#'
            if c.isdigit():
                if c == '0':
                    START = x, y
                else:
                    TARGET_NODES.add((x, y))
                    NODES[x, y] = frozenset(c)

INITIAL_STATE = State(START, 0, frozenset(chain(*NODES.values())))
SHORTEST = None
QUEUE = PriorityQueue()
QUEUE.put((0, INITIAL_STATE))
BEST_PATHS = defaultdict(lambda: defaultdict(lambda: float("inf")))

while not QUEUE.empty():
    d, next_best = QUEUE.get()
    print QUEUE.qsize(), d, next_best
    if len(next_best.left_to_visit) == 0:
        print "Found new candidate", next_best
        if SHORTEST:
            SHORTEST = min(SHORTEST, next_best.steps_so_far)
        else:
            SHORTEST = next_best.steps_so_far
        continue

    if SHORTEST and next_best.steps_so_far > SHORTEST:
        continue

    for option in generate_options(next_best):
        p, new_state = visit(option, next_best)
        BEST_PATHS[new_state.current_loc][new_state.left_to_visit] = new_state.steps_so_far
        QUEUE.put((p, new_state))

print "Part One:", SHORTEST

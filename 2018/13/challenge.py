#!/usr/bin/env pypy3

from itertools import count
import sys

TRACK_STRAIGHT = 1
TRACK_CURVE_RIGHT = 2
TRACK_CURVE_LEFT = 3
TRACK_INTERSECTION = 4

TRACK_TYPES = {
    '|': TRACK_STRAIGHT,
    '-': TRACK_STRAIGHT,
    '/': TRACK_CURVE_RIGHT,
    '\\': TRACK_CURVE_LEFT,
    '+': TRACK_INTERSECTION,
}

CART_LEFT = 1
CART_RIGHT = 2
CART_UP = 3
CART_DOWN = 4

CART_TYPES = {
    '<': CART_LEFT,
    '>': CART_RIGHT,
    '^': CART_UP,
    'v': CART_DOWN,
}


def load_grid(filename):
    with open(filename) as input_file:
        data = input_file.read()
    grid = {}
    carts = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c in TRACK_TYPES:
                grid[x, y] = TRACK_TYPES[c]
            if c in CART_TYPES:
                carts[x, y] = (CART_TYPES[c], 0)
    for pos in carts.keys():
        grid[pos] = TRACK_STRAIGHT
    return grid, carts


def print_grid(grid, carts):
    max_x = max(x for (x, y) in grid.keys())
    max_y = max(y for (x, y) in grid.keys())
    carts = {pos: direction for pos, (direction, turns) in carts.items()}
    sys.stdout.write('\n')
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in carts:
                if carts[x, y] == CART_RIGHT:
                    sys.stdout.write('>')
                elif carts[x, y] == CART_LEFT:
                    sys.stdout.write('<')
                elif carts[x, y] == CART_UP:
                    sys.stdout.write('^')
                elif carts[x, y] == CART_DOWN:
                    sys.stdout.write('v')
            elif (x, y) not in grid:
                sys.stdout.write(' ')
            elif grid[x,y] == TRACK_STRAIGHT:
                sys.stdout.write('+')
            elif grid[x,y] == TRACK_CURVE_RIGHT:
                sys.stdout.write('/')
            elif grid[x,y] == TRACK_CURVE_LEFT:
                sys.stdout.write('\\')
            elif grid[x,y] == TRACK_INTERSECTION:
                sys.stdout.write('*')
        sys.stdout.write('\n')
    sys.stdout.write('\n')


def next_cart(pos, cart, grid):
    x, y = pos
    direction, turns = cart
    if direction == CART_LEFT and grid[x, y] == TRACK_STRAIGHT:
        return (x - 1, y), direction, turns
    elif direction == CART_RIGHT and grid[x, y] == TRACK_STRAIGHT:
        return (x + 1, y), direction, turns
    elif direction == CART_UP and grid[x, y] == TRACK_STRAIGHT:
        return (x, y - 1), direction, turns
    elif direction == CART_DOWN and grid[x, y] == TRACK_STRAIGHT:
        return (x, y + 1), direction, turns
    elif grid[x, y] == TRACK_CURVE_RIGHT: # /
        if direction == CART_LEFT:
            return (x, y + 1), CART_DOWN, turns
        elif direction == CART_RIGHT:
            return (x, y - 1), CART_UP, turns
        elif direction == CART_UP:
            return (x + 1, y), CART_RIGHT, turns
        elif direction == CART_DOWN:
            return (x - 1, y), CART_LEFT, turns
    elif grid[x, y] == TRACK_CURVE_LEFT: # \
        if direction == CART_RIGHT:
            return (x, y + 1), CART_DOWN, turns
        elif direction == CART_LEFT:
            return (x, y - 1), CART_UP, turns
        elif direction == CART_DOWN:
            return (x + 1, y), CART_RIGHT, turns
        elif direction == CART_UP:
            return (x - 1, y), CART_LEFT, turns
    elif grid[x, y] == TRACK_INTERSECTION:
        if turns % 3 == 0:
            # turn left
            if direction == CART_LEFT:
                return (x, y + 1), CART_DOWN, turns + 1
            elif direction == CART_RIGHT:
                return (x, y - 1), CART_UP, turns + 1
            elif direction == CART_UP:
                return (x - 1, y), CART_LEFT, turns + 1
            elif direction == CART_DOWN:
                return (x + 1, y), CART_RIGHT, turns + 1
        elif turns % 3 == 1:
            # go straight
            if direction == CART_LEFT:
                return (x - 1, y), direction, turns + 1
            elif direction == CART_RIGHT:
                return (x + 1, y), direction, turns + 1
            elif direction == CART_UP:
                return (x, y - 1), direction, turns + 1
            elif direction == CART_DOWN:
                return (x, y + 1), direction, turns + 1
        elif turns % 3 == 2:
            # turn right
            if direction == CART_LEFT:
                return (x, y - 1), CART_UP, turns + 1
            elif direction == CART_RIGHT:
                return (x, y + 1), CART_DOWN, turns + 1
            elif direction == CART_UP:
                return (x + 1, y), CART_RIGHT, turns + 1
            elif direction == CART_DOWN:
                return (x - 1, y), CART_LEFT, turns + 1
    else:
        raise Exception()


def step(grid, carts, stop_on_crash=False):
    for pos in sorted(carts.keys(), key=lambda pos: (pos[1], pos[0])):
        if pos in carts:
            next_pos, direction, turns = next_cart(pos, carts[pos], grid)
            del carts[pos]
            if next_pos in carts:
                del carts[next_pos]
                if stop_on_crash:
                    return next_pos
            else:
                carts[next_pos] = (direction, turns)


def part_one(grid, initial_carts):
    carts = dict(initial_carts)
    for _ in count():
        crash_loc = step(grid, carts, stop_on_crash=True)
        if crash_loc is not None:
            return crash_loc


TEST_GRID, TEST_CARTS = load_grid('test.txt')
TEST_GRID2, TEST_CARTS2 = load_grid('test2.txt')
INITIAL_GRID, INITIAL_CARTS = load_grid('input.txt')


assert(part_one(TEST_GRID, TEST_CARTS) == (7, 3))
print("Part One: {},{}".format(*part_one(INITIAL_GRID, INITIAL_CARTS)))


def part_two(grid, initial_carts):
    carts = dict(initial_carts)
    while len(carts) > 1:
        step(grid, carts)
    return list(carts.keys())[0]


assert(part_two(TEST_GRID2, TEST_CARTS2) == (6,4))
print("Part Two: {},{}".format(*part_two(INITIAL_GRID, INITIAL_CARTS)))

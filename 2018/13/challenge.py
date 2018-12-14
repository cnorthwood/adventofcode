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
    carts = set()
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c in TRACK_TYPES:
                grid[x, y] = TRACK_TYPES[c]
            if c in CART_TYPES:
                carts.add(((x, y), CART_TYPES[c], 0))
    for pos, cart_type, turns in carts:
        grid[pos] = TRACK_STRAIGHT
    return grid, carts


def print_grid(grid, carts):
    max_x = max(x for (x, y) in grid.keys())
    max_y = max(y for (x, y) in grid.keys())
    carts = {pos: direction for pos, direction, turns in carts}
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


def next_cart(cart, grid):
    (x, y), direction, turns = cart
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


def step(grid, carts):
    return {next_cart(cart, grid) for cart in carts}


def find_crash(grid, carts):
    for _ in count():
        # print_grid(grid, carts)
        for this_cart in carts:
            other_cart_positions = {pos for (pos, direction, turns) in carts - {this_cart}}
            if this_cart[0] in other_cart_positions:
                return this_cart[0], {cart for cart in carts if cart[0] != this_cart[0]}
        carts = step(grid, carts)


TEST_GRID, TEST_CARTS = load_grid('test.txt')
TEST_GRID2, TEST_CARTS2 = load_grid('test2.txt')
INITIAL_GRID, INITIAL_CARTS = load_grid('input.txt')


assert(find_crash(TEST_GRID, TEST_CARTS)[0] == (7, 3))
print("Part One: {},{}".format(*find_crash(INITIAL_GRID, INITIAL_CARTS)[0]))


def remove_all_crashes(grid, carts):
    while len(carts) > 1:
        carts = find_crash(grid, carts)[1]
    return carts.pop()[0]


assert(remove_all_crashes(TEST_GRID2, TEST_CARTS2) == (6,4))
print("Part Two: {},{}".format(*remove_all_crashes(INITIAL_GRID, INITIAL_CARTS)))

#!/usr/bin/env -S pypy3 -S

from collections import Counter
from itertools import count
from math import ceil, floor, prod
import re

def load_input(input_filename):
    # generator of (x, y, dx, dy)
    input_re = re.compile(r'p=(?P<x>\d+),(?P<y>\d+) v=(?P<dx>-?\d+),(?P<dy>-?\d+)')
    with open(input_filename) as input_file:
        for line in input_file:
            if not line.strip():
                continue
            match = input_re.match(line)
            yield int(match.group("x")), int(match.group("y")), int(match.group("dx")), int(match.group("dy"))


def move(drone, n):
    x, y, dx, dy = drone
    return (x + dx * n) % MAX_X, (y + dy * n) % MAX_Y


def grid(drones, n):
    return Counter(move(drone, n) for drone in drones)


def quadrant_count(grid):
    qx = MAX_X / 2
    qy = MAX_Y / 2
    return prod([
        sum(count for (x, y), count in grid.items() if x < floor(qx) and y < floor(qy)), # top left
        sum(count for (x, y), count in grid.items() if x >= ceil(qx) and y < floor(qy)), # top right
        sum(count for (x, y), count in grid.items() if x < floor(qx) and y >= ceil(qy)), # bottom left
        sum(count for (x, y), count in grid.items() if x >= ceil(qx) and y >= ceil(qy)), # bottom right
    ])


def is_tree(grid):
    # cba doing this visually, ripped it off from Shane and the sub-Reddit - 7 1s in a row is a tree
    return any(all(grid.get((x, y)) == 1 for x in range(sx, sx + 7)) for sx in range(MAX_X) for y in range(MAX_Y + 1))


def find_easter_egg(drones):
    for i in count():
        if is_tree(grid(drones, i)):
            return i

MAX_X = 101
MAX_Y = 103
INPUT = list(load_input("input.txt"))

print(f"Part One: {quadrant_count(grid(INPUT, 100))}")
print(f"Part Two: {find_easter_egg(INPUT)}")

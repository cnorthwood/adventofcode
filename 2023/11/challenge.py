#!/usr/bin/env python3
from itertools import combinations


def load_input(filename):
    galaxies = set()
    with open(filename) as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line):
                if c == "#":
                    galaxies.add((x, y))
    return galaxies


def expand_universe(universe, mag_factor):
    cols_to_expand = []
    rows_to_expand = []
    max_x = max(galaxy[0] for galaxy in universe)
    max_y = max(galaxy[1] for galaxy in universe)
    for x in range(max_x):
        if all((x, y) not in universe for y in range(max_y)):
            cols_to_expand.append(x)
    for y in range(max_y):
        if all((x, y) not in universe for x in range(max_x)):
            rows_to_expand.append(y)

    return {(x + sum(mag_factor-1 for col in cols_to_expand if x > col), y + sum(mag_factor-1 for row in rows_to_expand if y > row)) for x, y in universe}


def manhattan(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


UNIVERSE = load_input("input.txt")
print(f"Part One: {sum(manhattan(a, b) for a, b in combinations(expand_universe(UNIVERSE, mag_factor=2), 2))}")
print(f"Part Two: {sum(manhattan(a, b) for a, b in combinations(expand_universe(UNIVERSE, 1_000_000), 2))}")

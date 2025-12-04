#!/usr/bin/env python3

from functools import cache


def load_input(filename):
    with open(filename) as input_file:
        return frozenset({(x, y) for y, line in enumerate(input_file.readlines()) for x, c in enumerate(line.strip()) if c == "@"})


@cache
def neighbours(position):
    x, y = position
    return frozenset({
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    })


def num_neighbours(position, locations):
    return sum(1 for neighbour in neighbours(position) if neighbour in locations)


ROLL_LOCATIONS = load_input("input.txt")
print(f"Part One: {sum(1 for position in ROLL_LOCATIONS if num_neighbours(position, ROLL_LOCATIONS) < 4)}")

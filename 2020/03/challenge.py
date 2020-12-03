#!/usr/bin/env python3
from math import prod

with open("input.txt") as puzzle_input:
    INPUT = [[c == "#" for c in line.strip()] for line in puzzle_input]

with open("test.txt") as test_input:
    TEST_INPUT = [[c == "#" for c in line.strip()] for line in test_input]


def trees_collided(x, y, dx, dy, forest):
    if y >= len(forest):
        return 0
    if forest[y][x % len(forest[y])]:
        return 1 + trees_collided(x + dx, y + dy, dx, dy, forest)
    else:
        return trees_collided(x + dx, y + dy, dx, dy, forest)


assert trees_collided(0, 0, 3, 1, TEST_INPUT) == 7
print(f"Part One: {trees_collided(0, 0, 3, 1, INPUT)}")
print(f"Part Two: {prod(trees_collided(0, 0, dx, dy, INPUT) for dx, dy in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])}")

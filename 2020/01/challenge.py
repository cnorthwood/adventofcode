#!/usr/bin/env python3
from itertools import combinations
from math import prod

with open("input.txt") as puzzle_input:
    INPUT = [int(line) for line in puzzle_input]


def find_combo(values, n, target=2020):
    for vs in combinations(values, n):
        if sum(vs) == target:
            return prod(vs)


print(f"Part One: {find_combo(INPUT, 2)}")
print(f"Part Two: {find_combo(INPUT, 3)}")

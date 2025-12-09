#!/usr/bin/env python3

from itertools import combinations


def load_input(filename):
    with open(filename) as input_file:
        return {tuple(map(int, line.strip().split(","))) for line in input_file.readlines()}


def area(a, b):
    return abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1)


INPUT = load_input("input.txt")
print(f"Part One: {max(area(a, b) for a, b in combinations(INPUT, 2))}")

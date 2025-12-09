#!/usr/bin/env python3

from itertools import combinations

from shapely import Polygon, box


def load_input(filename):
    with open(filename) as input_file:
        return [tuple(map(int, line.strip().split(","))) for line in input_file.readlines()]


def area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def part_2(points):
    shape = Polygon(points)
    for a, b in sorted(combinations(points, 2), key=lambda pair: area(*pair), reverse=True):
        rect = box(*a, *b)
        if shape.covers(rect):
            return area(a, b)


INPUT = load_input("input.txt")
print(f"Part One: {max(area(a, b) for a, b in combinations(INPUT, 2))}")
print(f"Part Two: {part_2(INPUT)}")

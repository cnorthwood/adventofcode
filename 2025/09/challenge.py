#!/usr/bin/env python3

from functools import cache
from itertools import combinations


def load_input(filename):
    with open(filename) as input_file:
        return [tuple(map(int, line.strip().split(","))) for line in input_file.readlines()]


def area(a, b):
    return abs(a[0] - b[0] + 1) * abs(a[1] - b[1] + 1)


def build_bounds(points):
    bounds = set()
    for (ax, ay), (bx, by) in zip(points, points[1:] + [points[0]]):
        if ax == bx:
            # filling vertically
            for y in range(ay, by, -1 if ay > by else 1):
                bounds.add((ax, y))
        elif ay == by:
            # filling horizontally
            for x in range(ax, bx, -1 if ax > bx else 1):
                bounds.add((x, ay))
        else:
            raise ValueError()
    return frozenset(bounds)


@cache
def inside_bounds(point, bounds):
    if point in bounds:
        return True
    x, y = point
    # use the winding number algorithm, cast a ray towards the origin and count the number of intersections made
    # https://lazyjobseeker.github.io/en/posts/winding-number-algorithm/
    edge_crosses = sum(1 for d in range(min(x, y) - MIN_BOUND) if (x - d, y - d) in bounds)
    return edge_crosses % 2 == 1


def all_inside_bounds(a, b, bounds):
    ax, ay = a
    bx, by = b
    top_left = (min(ax, bx), min(ay, by))
    top_right = (max(ax, bx), min(ay, by))
    bottom_right = (max(ax, bx), max(ay, by))
    bottom_left = (min(ax, bx), max(ay, by))
    return all(inside_bounds(point, bounds) for point in build_bounds([top_left, top_right, bottom_right, bottom_left]))


def part_2(points, bounds):
    for a, b in sorted(combinations(points, 2), key=lambda pair: area(*pair), reverse=True):
        if all_inside_bounds(a, b, bounds):
            return area(a, b)


INPUT = load_input("test.txt")
print(f"Part One: {max(area(a, b) for a, b in combinations(INPUT, 2))}")

BOUNDS = build_bounds(INPUT)
MIN_BOUND = min(min(x for x, _ in BOUNDS), min(y for _, y in BOUNDS)) - 1
print(f"Part Two: {part_2(INPUT, BOUNDS)}")

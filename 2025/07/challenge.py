#!/usr/bin/env python3

from functools import cache


def load_input(filename):
    with open(filename) as input_file:
        lines = input_file.readlines()
    start_x = lines[0].index("S")
    splitter_xs = tuple(frozenset({x for x, c in enumerate(line) if c == "^"}) for line in lines)
    return start_x, splitter_xs


def part_one(start_x, splitter_xs):
    n_splits = 0
    rays = {start_x}
    for row_splitter_xs in splitter_xs:
        next_rays = set()
        for ray_x in rays:
            if ray_x in row_splitter_xs:
                next_rays.add(ray_x - 1)
                next_rays.add(ray_x + 1)
                n_splits += 1
            else:
                next_rays.add(ray_x)
        rays = next_rays
    return n_splits


@cache
def part_two(start_x, splitter_xs):
    if len(splitter_xs) == 0:
        return 1
    if start_x in splitter_xs[0]:
        return part_two(start_x - 1, splitter_xs[1:]) + part_two(start_x + 1, splitter_xs[1:])
    else:
        return part_two(start_x, splitter_xs[1:])


START_X, SPLITTER_XS = load_input("input.txt")
print(f"Part One: {part_one(START_X, SPLITTER_XS)}")
print(f"Part Two: {part_two(START_X, SPLITTER_XS)}")

#!/usr/bin/env python3


def load_input(filename):
    with open(filename) as input_file:
        lines = input_file.readlines()
    start_x = lines[0].index("S")
    splitter_xs = [{x for x, c in enumerate(line) if c == "^"} for line in lines]
    return start_x, splitter_xs


def simulate(start_x, splitter_xs):
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

START_X, SPLITTER_XS = load_input("input.txt")
print(f"Part One: {simulate(START_X, SPLITTER_XS)}")

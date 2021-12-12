#!/usr/bin/env python3
from collections import defaultdict
from math import prod


def load_input(filename):
    heightmap = {}
    with open(filename) as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line.strip()):
                heightmap[x, y] = int(c)
    return heightmap


def adjacent(x, y):
    yield x - 1, y
    yield x + 1, y
    yield x, y + 1
    yield x, y - 1


def is_low_point(heightmap, x, y):
    return all(heightmap[neighbour] > heightmap[x, y] for neighbour in adjacent(x, y) if neighbour in heightmap)


def populate_low_point_for_coord(basins, coord, heightmap):
    for adjacent_coord in adjacent(*coord):
        if adjacent_coord in basins or adjacent_coord not in heightmap or heightmap.get(adjacent_coord) == 9:
            continue
        basins[adjacent_coord] = basins[coord]
        populate_low_point_for_coord(basins, adjacent_coord, heightmap)


HEIGHTMAP = load_input("input.txt")
LOW_POINTS = {(x, y): (x, y) for x, y in HEIGHTMAP.keys() if is_low_point(HEIGHTMAP, x, y)}
print(f"Part One: {sum(1 + HEIGHTMAP[x, y] for x, y in LOW_POINTS.keys())}")
for low_point in list(LOW_POINTS.keys()):
    populate_low_point_for_coord(LOW_POINTS, low_point, HEIGHTMAP)
BASINS = defaultdict(set)
for coord in HEIGHTMAP:
    if coord in LOW_POINTS:
        BASINS[LOW_POINTS[coord]].add(coord)
print(f"Part Two: {prod(len(coords) for coords in sorted(BASINS.values(), key=len, reverse=True)[:3])}")

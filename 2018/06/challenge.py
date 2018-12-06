#!/usr/bin/env pypy3

from collections import Counter
from itertools import product


def load_coords(filename):
    with open(filename) as input_file:
        return set(tuple(map(int, line.split(','))) for line in input_file.read().strip().splitlines())


TEST = load_coords('test.txt')
INPUT = load_coords('input.txt')


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def grid_edges(coords):
    min_x = min(x for x, y in coords)
    max_x = max(x for x, y in coords)
    min_y = min(y for x, y in coords)
    max_y = max(y for x, y in coords)

    return min_x, max_x, min_y, max_y


def build_grid(coords):
    min_x, max_x, min_y, max_y = grid_edges(coords)
    all_distances = {
        (x, y): {
            coord: manhattan((x, y), coord) for coord in coords
        } for x, y in product(range(min_x, max_x), range(min_y, max_y))
    }
    grid = {}
    for coord, distances in all_distances.items():
        sorted_distances = sorted(distances.items(), key=lambda k: k[1])
        closest_coord, distance = sorted_distances[0]
        if distance == sorted_distances[1][1]:
            grid[coord] = None
        else:
            grid[coord] = closest_coord
    return grid


TEST_GRID = build_grid(TEST)
GRID = build_grid(INPUT)


def largest_area(grid):
    areas = Counter()
    for coord, region in grid.items():
        if region is not None:
            areas[region] += 1
    return areas.most_common(1)[0][1]


assert(largest_area(TEST_GRID) == 17)
print("Part One: {}".format(largest_area(GRID)))

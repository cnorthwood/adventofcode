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
        } for x, y in product(range(min_x, max_x + 1), range(min_y, max_y + 1))
    }
    grid = {}
    infinite_regions = set()
    for coord, distances in all_distances.items():
        sorted_distances = sorted(distances.items(), key=lambda k: k[1])
        closest_coord, distance = sorted_distances[0]
        if distance == sorted_distances[1][1]:
            closest_coord = None
        grid[coord] = (closest_coord, sum(distances.values()))
        is_infinite = not (min_x < coord[0] < max_x and min_y < coord[1] < max_y)
        if is_infinite:
            infinite_regions.add(closest_coord)
    return grid, infinite_regions


TEST_GRID, TEST_INFINITE_REGIONS = build_grid(TEST)
GRID, INFINITE_REGIONS = build_grid(INPUT)


def largest_area(grid, infinite_regions):
    areas = Counter()
    for coord, (region, _) in grid.items():
        if region is not None and region not in infinite_regions:
            areas[region] += 1
    return areas.most_common(1)[0][1]


assert(largest_area(TEST_GRID, TEST_INFINITE_REGIONS) == 17)
print("Part One: {}".format(largest_area(GRID, INFINITE_REGIONS)))


def safe_region(grid, threshold):
    c = 0
    for coord, (region, size) in grid.items():
        if size < threshold:
            c += 1
    return c


assert(safe_region(TEST_GRID, 32) == 16)
print("Part Two: {}".format(safe_region(GRID, 10000)))

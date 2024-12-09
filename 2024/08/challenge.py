#!/usr/bin/env -S pypy3 -S

from collections import defaultdict
from itertools import permutations


def load_input(input_filename):
    antenna_locations = defaultdict(set)
    with open(input_filename) as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line.strip()):
                if c != ".":
                    antenna_locations[c].add((x, y))
    return antenna_locations


def find_antinodes(locations):
    for loc_a, loc_b in permutations(locations, r=2):
        dx = loc_a[0] - loc_b[0]
        dy = loc_a[1] - loc_b[1]
        antinode = loc_b[0] - dx, loc_b[1] - dy
        yield antinode


def all_antinodes_for_antenna(antenna_locations):
    antinode_locations = {}
    for antenna, locations in antenna_locations.items():
        antinode_locations[antenna] = set(find_antinodes(locations))
    return antinode_locations


def antinodes_in_bounds(antinode_locations, max_x, max_y):
    all_antinodes = set()
    for antinodes in antinode_locations.values():
        all_antinodes |= antinodes
    return sum(1 for x, y in all_antinodes if 0 <= x <= max_x and 0 <= y <= max_y)


ANTENNA_LOCATIONS = load_input("input.txt")
MAX_X = max(max(loc[0] for loc in locations) for locations in ANTENNA_LOCATIONS.values())
MAX_Y = max(max(loc[1] for loc in locations) for locations in ANTENNA_LOCATIONS.values())

print(f"Part One: {antinodes_in_bounds(all_antinodes_for_antenna(ANTENNA_LOCATIONS), MAX_X, MAX_Y)}")

#!/usr/bin/env -S pypy3 -S

from collections import defaultdict
from itertools import permutations, count


def load_input(input_filename):
    antenna_locations = defaultdict(set)
    with open(input_filename) as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line.strip()):
                if c != ".":
                    antenna_locations[c].add((x, y))
    return antenna_locations


ANTENNA_LOCATIONS = load_input("input.txt")
MAX_X = max(max(loc[0] for loc in locations) for locations in ANTENNA_LOCATIONS.values())
MAX_Y = max(max(loc[1] for loc in locations) for locations in ANTENNA_LOCATIONS.values())


def node_in_bounds(node):
    return 0 <= node[0] <= MAX_X and 0 <= node[1] <= MAX_Y


def find_antinodes(locations):
    for loc_a, loc_b in permutations(locations, r=2):
        dx = loc_a[0] - loc_b[0]
        dy = loc_a[1] - loc_b[1]
        antinode = loc_b[0] - dx, loc_b[1] - dy
        if not node_in_bounds(antinode):
            continue
        yield antinode


def find_harmonics(locations):
    for loc_a, loc_b in permutations(locations, r=2):
        for i in count(start=1):
            dx = loc_a[0] - loc_b[0]
            dy = loc_a[1] - loc_b[1]
            antinode = loc_a[0] - i*dx, loc_a[1] - i*dy
            if not node_in_bounds(antinode):
                break
            yield antinode


def all_antinodes(antenna_locations, finder):
    antinode_locations = set()
    for antenna, locations in antenna_locations.items():
        antinode_locations |= set(finder(locations))
    return antinode_locations


print(f"Part One: {len(all_antinodes(ANTENNA_LOCATIONS, finder=find_antinodes))}")
print(f"Part Two: {len(all_antinodes(ANTENNA_LOCATIONS, finder=find_harmonics))}")

#!/usr/bin/env pypy3

from collections import defaultdict, deque


def build_orbits(orbits):
    orbit_tree = defaultdict(list)
    orbit_graph = defaultdict(list)
    for orbitee, orbiter in orbits:
        orbit_tree[orbitee].append(orbiter)
        orbit_graph[orbitee].append(orbiter)
        orbit_graph[orbiter].append(orbitee)
    return orbit_tree, orbit_graph


def count_orbiters(tree, leaf="COM", depth=0):
    return depth + sum(count_orbiters(tree, child, depth + 1) for child in tree[leaf])


def shortest_path_length(tree):
    queue = deque([["YOU"]])
    while queue:
        path = queue.popleft()
        for child in tree[path[-1]]:
            if child in path:
                continue
            if child == "SAN":
                return len(path) - 2
            else:
                queue.append(path + [child])


# with open("test.txt") as input_file:
#     TEST_ORBITS, _ = build_orbits(orbit.strip().split(")") for orbit in input_file.readlines())

with open("input.txt") as input_file:
    ORBITS, ORBITINGS = build_orbits(orbit.strip().split(")") for orbit in input_file.readlines())


# assert(count_orbiters(TEST_ORBITS) == 42)
print(f"Part One: {count_orbiters(ORBITS)}")
print(f"Part Two: {shortest_path_length(ORBITINGS)}")

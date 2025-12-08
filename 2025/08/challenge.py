#!/usr/bin/env python3

from collections import defaultdict
from itertools import count, combinations
from math import dist, prod


def load_input(filename):
    with open(filename) as input_file:
        return {tuple(int(coord) for coord in line.strip().split(",")) for line in input_file.readlines()}


def init_network(coords):
    return {coord: None for coord in coords}, count()


def closest_pairs(coords):
    return sorted(combinations(coords, 2), key=lambda pair: dist(*pair))


def connect_circuit(a, b, networks, network_id_generator):
    if networks[a] is None and networks[b] is None:
        networks[a] = networks[b] = next(network_id_generator)
    elif networks[a] is not None and networks[b] is None:
        networks[b] = networks[a]
    elif networks[a] is None and networks[b] is not None:
        networks[a] = networks[b]
    else:
        merge_target = networks[a]
        merge_from = networks[b]
        for coord in networks.keys():
            if networks[coord] == merge_from:
                networks[coord] = merge_target


def partition_networks(networks):
    clusters = defaultdict(set)
    for coord, network_id in networks.items():
        if network_id is None:
            continue
        clusters[network_id].add(coord)
    return clusters.values()


def part_one(coords, n=1000):
    networks, network_id_generator = init_network(coords)
    for a, b in closest_pairs(coords)[:n]:
        connect_circuit(a, b, networks, network_id_generator)

    network_sizes = [len(network) for network in partition_networks(networks)]
    return prod(sorted(network_sizes, reverse=True)[:3])


def part_two(coords):
    networks, network_id_generator = init_network(coords)
    for a, b in closest_pairs(coords):
        connect_circuit(a, b, networks, network_id_generator)
        if len(set(networks.values())) == 1:
            return a[0] * b[0]


# print(f"Test: {part_two(load_input('test.txt'))}")
INPUT = load_input("input.txt")
print(f"Part One: {part_one(INPUT)}")
print(f"Part Two: {part_two(INPUT)}")

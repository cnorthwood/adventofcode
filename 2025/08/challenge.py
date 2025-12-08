#!/usr/bin/env python3

from collections import defaultdict
from itertools import count, combinations
from math import dist, prod


def load_input(filename):
    with open(filename) as input_file:
        return {tuple(int(coord) for coord in line.strip().split(",")) for line in input_file.readlines()}


def generate_network_id():
    yield from count()
NETWORK_ID_GENERATOR = generate_network_id()


def connect_networks(coords, n=1000):
    networks = {coord: None for coord in coords}
    for a, b in sorted(combinations(coords, 2), key=lambda pair: dist(*pair))[:n]:
        if networks[a] is None and networks[b] is None:
            networks[a] = networks[b] = next(NETWORK_ID_GENERATOR)
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
    return networks


def part_one(networks):
    clusters = defaultdict(set)
    for coord, network_id in networks.items():
        if network_id is None:
            continue
        clusters[network_id].add(coord)
    cluster_sizes = [len(cluster) for cluster in clusters.values()]
    return prod(sorted(cluster_sizes, reverse=True)[:3])


# print(f"Test: {part_one(connect_networks(load_input('test.txt'), n=10))}")
print(f"Part One: {part_one(connect_networks(load_input('input.txt')))}")

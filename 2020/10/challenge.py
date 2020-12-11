#!/usr/bin/env python3
from collections import defaultdict

with open("input.txt") as input_file:
    INPUT = [int(line.strip()) for line in input_file]
TARGET_JOLTS = max(INPUT) + 3

CHAIN = [0] + list(sorted(INPUT)) + [TARGET_JOLTS]


def find_part_one(chain):
    d1s = 0
    d3s = 0
    for i in range(len(chain)):
        d = chain[i] - chain[i-1]
        if d == 1:
            d1s += 1
        if d == 3:
            d3s += 1
    return d1s * d3s


def fill_paths_forward(chain):
    paths_to = defaultdict(int)
    paths_to[0] = 1
    all_adapters = set(chain)
    for adapter_in_chain in chain:
        for d in range(1, 4):
            next_adapter = adapter_in_chain + d
            if next_adapter not in all_adapters:
                continue
            paths_to[next_adapter] += paths_to[adapter_in_chain]
    return paths_to[chain[-1]]


print(f"Part One: {find_part_one(CHAIN)}")
print(f"Part Two: {fill_paths_forward(CHAIN)}")

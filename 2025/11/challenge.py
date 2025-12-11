#!/usr/bin/env python3

from functools import cache


def load_input(filename):
    graph = {}
    with open(filename) as input_file:
        for line in input_file.readlines():
            machine, outs = line.strip().split(": ")
            graph[machine] = outs.split()
    return graph


GRAPH = load_input("input.txt")


@cache
def find_paths_from(start, end):
    if start == end:
        return 1
    else:
        return sum(find_paths_from(next_step, end) for next_step in GRAPH.get(start, []))


print(f"Part One: {find_paths_from('you', 'out')}")
print(f"Part Two: {find_paths_from('svr', 'fft') * find_paths_from('fft', 'dac') * find_paths_from('dac', 'out')}")

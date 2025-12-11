#!/usr/bin/env python3

from collections import deque


def load_input(filename):
    graph = {}
    with open(filename) as input_file:
        for line in input_file.readlines():
            machine, outs = line.strip().split(": ")
            graph[machine] = outs.split()
    return graph


INPUT = load_input("input.txt")


def find_paths(graph, start="you", end="out"):
    complete_paths = set()
    current_threads = {(start,)}

    while len(current_threads) > 0:
        thread = current_threads.pop()
        if thread[-1] == end:
            complete_paths.add(thread)
            continue

        for next_link in graph[thread[-1]]:
            current_threads.add(thread + (next_link,))

    return len(complete_paths)


print(f"Part One: {find_paths(INPUT)}")

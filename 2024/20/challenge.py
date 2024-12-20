#!/usr/bin/env -S pypy3 -S

from functools import cache
from heapq import heapify, heappop, heappush
from math import inf


def load_input(input_filename):
    grid = {}
    with open(input_filename) as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line.strip()):
                grid[x, y] = c

    start = next(coord for coord, c in grid.items() if c == "S")
    target = next(coord for coord, c in grid.items() if c == "E")
    valid_squares = frozenset({coord for coord, c in grid.items() if c != "#"})
    return start, target, valid_squares


DIRECTIONS = {
    "N":  (0, -1),
    "S":  (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}


def generate_neighbours(coord):
    for direction in DIRECTIONS.values():
        yield coord[0] + direction[0], coord[1] + direction[1]


def dijkstra(start, valid_squares):
    costs = {coord: inf for coord in valid_squares}
    costs[start] = 0
    queue = [(0, start)]
    heapify(queue)

    visited = set()

    while queue:
        cost, coord = heappop(queue)
        if coord in visited:
            continue
        visited.add(coord)

        for neighbour in generate_neighbours(coord):
            if neighbour not in valid_squares:
                continue
            next_cost = cost + 1
            if next_cost < costs[neighbour]:
                costs[neighbour] = next_cost
                heappush(queue, (next_cost, neighbour))

    return costs


def backtrack(target, costs):
    predecessors = {coord: None for coord in costs}
    for coord, cost in costs.items():
        for neighbour in generate_neighbours(coord):
            if neighbour not in costs:
                continue
            if costs[neighbour] == cost + 1:
                predecessors[neighbour] = coord

    path = []
    current_node = target
    while current_node:
        path.append(current_node)
        current_node = predecessors[current_node]

    return path


def generate_glitches(coord, valid_route):
    for glitch_step1 in generate_neighbours(coord):
        for glitch_step2 in generate_neighbours(glitch_step1):
            if glitch_step2 in valid_route:
                yield (glitch_step1, glitch_step2)


def part1(start, target, valid_squares):
    costs = dijkstra(start, valid_squares)
    path = backtrack(target, costs)
    valid_route = set(path)

    good_glitches = set()
    for coord in path:
        for glitch_step1, glitch_step2 in generate_glitches(coord, valid_route):
            if costs[glitch_step2] - costs[coord] > 100:
                good_glitches.add((glitch_step1, glitch_step2))
    return len(good_glitches)


START, TARGET, VALID_SQUARES = load_input("input.txt")
print(f"Part One: {part1(START, TARGET, VALID_SQUARES)}")

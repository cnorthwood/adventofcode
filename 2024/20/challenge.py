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


@cache
def generate_cheats(coord, valid_route, cheat_length):
    cheat_ends = set()
    if coord in valid_route:
        cheat_ends.add(coord)
    if cheat_length > 0:
        for cheat_step in generate_neighbours(coord):
            cheat_ends |= generate_cheats(cheat_step, valid_route, cheat_length - 1)
    return cheat_ends


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def time_saved(costs, cheat_start, cheat_end):
    return costs[cheat_end] - costs[cheat_start] - manhattan(cheat_start, cheat_end)



def main(start, target, valid_squares, cheat_length, good_cheat_threshold=100):
    costs = dijkstra(start, valid_squares)
    path = backtrack(target, costs)
    valid_route = frozenset(path)

    good_cheats = {(cheat_start, cheat_end) for cheat_start in valid_route for cheat_end in generate_cheats(cheat_start, valid_route, cheat_length) if time_saved(costs, cheat_start, cheat_end) >= good_cheat_threshold}
    return len(good_cheats)


START, TARGET, VALID_SQUARES = load_input("input.txt")
print(f"Part One: {main(START, TARGET, VALID_SQUARES, cheat_length=2)}")
print(f"Part Two: {main(START, TARGET, VALID_SQUARES, cheat_length=20)}")

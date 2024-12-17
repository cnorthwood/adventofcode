#!/usr/bin/env -S python3 -S

from heapq import heapify, heappop, heappush
from math import inf


DIRECTIONS = {
    "N":  (0, -1),
    "S":  (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}


TURNS = {
    "N": {"E", "W"},
    "S": {"E", "W"},
    "E": {"N", "S"},
    "W": {"N", "S"},
}


def load_input(input_filename):
    grid = {}
    with open(input_filename) as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line.strip()):
                grid[x, y] = c

    return grid


def apply_direction(coord, direction):
    return coord[0] + DIRECTIONS[direction][0], coord[1] + DIRECTIONS[direction][1]


def generate_neighbours(coord, direction, valid_squares):
    if (next_step := apply_direction(coord, direction)) in valid_squares:
        yield 1, (next_step, direction)
    for turn in TURNS[direction]:
        if (next_step := apply_direction(coord, turn)) in valid_squares:
            yield 1001, (next_step, turn)


def dijkstra_lowest_cost(grid):
    valid_squares = {coord for coord, c in grid.items() if c != "#"}
    start = next(coord for coord in valid_squares if grid[coord] == "S")
    target = next(coord for coord in valid_squares if grid[coord] == "E")
    costs = {(coord, direction): inf for direction in DIRECTIONS for coord in valid_squares}
    costs[start, "E"] = 0

    queue = [(0, (start, "E"))]
    heapify(queue)

    visited = set()

    while queue:
        cost, (coord, direction) = heappop(queue)
        if (coord, direction) in visited:
             continue
        visited.add((coord, direction))

        for step_cost, neighbour in generate_neighbours(coord, direction, valid_squares):
            next_cost = cost + step_cost
            if next_cost < costs[neighbour]:
                costs[neighbour] = next_cost
                heappush(queue, (next_cost, neighbour))

    return min(cost for (coord, direction), cost in costs.items() if coord == target)


INPUT = load_input("input.txt")
print(f"Part One: {dijkstra_lowest_cost(INPUT)}")

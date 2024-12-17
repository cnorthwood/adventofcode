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


def dijkstra(start, grid):
    valid_squares = {coord for coord, c in grid.items() if c != "#"}
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

    return costs


def build_predecessors(grid, costs):
    valid_squares = {coord for coord, c in grid.items() if c != "#"}
    predecessors = {(coord, direction): set() for direction in DIRECTIONS for coord in valid_squares}

    for (coord, direction), cost in costs.items():
        for step_cost, neighbour_state in generate_neighbours(coord, direction, valid_squares):
            if costs[neighbour_state] == cost + step_cost:
                predecessors[neighbour_state].add((coord, direction))

    return predecessors


def backtrack(state, predecessors):
    path = {state[0]}

    for predecessor in predecessors[state]:
        path.add(predecessor[0])
        path.update(backtrack(predecessor, predecessors))

    return path


def valid_end_states(target, costs):
    lowest_cost = min(cost for (coord, direction), cost in costs.items() if coord == target)
    return lowest_cost, {(coord, direction) for (coord, direction), cost in costs.items() if coord == target and cost == lowest_cost}


INPUT = load_input("input.txt")
START = next(coord for coord, c in INPUT.items() if c == "S")
TARGET = next(coord for coord, c in INPUT.items() if c == "E")
COSTS = dijkstra(START, INPUT)
LOWEST_COST, VALID_ENDINGS = valid_end_states(TARGET, COSTS)
PREDECESSORS = build_predecessors(INPUT, COSTS)

print(f"Part One: {LOWEST_COST}")
print(f"Part Two: {len(set.union(*(backtrack(state, PREDECESSORS) for state in VALID_ENDINGS)))}")

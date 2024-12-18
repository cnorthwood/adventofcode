#!/usr/bin/env -S pypy3 -S

from heapq import heapify, heappop, heappush
from math import inf


def load_input(input_filename):
    with open(input_filename) as input_file:
        for line in input_file:
            x, y = line.strip().split(",")
            yield int(x), int(y)


def build_valid_squares(falling_bytes, l=1024):
    corrupted_squares = {coord for coord in falling_bytes[:l]}
    return {(x, y) for x in range(W) for y in range(H) if (x, y) not in corrupted_squares}


def generate_neighbours(coord, valid_squares):
    if (next_square := (coord[0] - 1, coord[1])) in valid_squares:
        yield next_square
    if (next_square := (coord[0] + 1, coord[1])) in valid_squares:
        yield next_square
    if (next_square := (coord[0], coord[1] - 1)) in valid_squares:
        yield next_square
    if (next_square := (coord[0], coord[1] + 1)) in valid_squares:
        yield next_square


def dijkstra(corrupted_squares):
    start = (0, 0)
    target = (W-1, H-1)
    valid_squares = {(x, y) for x in range(W) for y in range(H) if (x, y) not in corrupted_squares}

    costs = {coord: inf for coord in valid_squares}
    queue = [(0, start)]
    heapify(queue)

    visited = set()

    while queue:
        cost, coord = heappop(queue)
        if coord in visited:
            continue
        visited.add(coord)

        for neighbour in generate_neighbours(coord, valid_squares):
            next_cost = cost + 1
            if next_cost < costs[neighbour]:
                costs[neighbour] = next_cost
                heappush(queue, (next_cost, neighbour))

    return costs[target]


def part2(falling_bytes):
    corrupted_squares = set(falling_bytes[:1024])
    for byte in falling_bytes[1024:]:
        corrupted_squares.add(byte)
        if dijkstra(corrupted_squares) == inf:
            return byte


W = 71
H = 71
INPUT = list(load_input("input.txt"))
print(f"Part One: {dijkstra(INPUT[:1024])}")
print(f"Part Two: {','.join(map(str, part2(INPUT)))}")

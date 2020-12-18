#!/usr/bin/env python3

from itertools import chain


def generate_neighbours_3d(coord):
    x, y, z = coord
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if dx == dy == dz == 0:
                    continue
                yield x + dx, y + dy, z + dz


def generate_neighbours_4d(coord):
    x, y, z, w = coord
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dw == dx == dy == dz == 0:
                        continue
                    yield x + dx, y + dy, z + dz, w + dw


def iterate(last_generation, neighbours_func):
    next_generation = set()
    for active_cube in last_generation:
        if 2 <= sum(1 for neighbour in neighbours_func(active_cube) if neighbour in last_generation) <= 3:
            next_generation.add(active_cube)
    for to_consider in chain.from_iterable(neighbours_func(coord) for coord in last_generation):
        if to_consider in last_generation:
            continue
        if sum(1 for neighbour in neighbours_func(to_consider) if neighbour in last_generation) == 3:
            next_generation.add(to_consider)
    return next_generation


def run(start_grid, neighbours_func, iterations=6):
    grid = {coord for coord in start_grid}
    for _ in range(iterations):
        grid = iterate(grid, neighbours_func)
    return len(grid)


with open("input.txt") as input_file:
    INPUT_3D = set()
    INPUT_4D = set()
    for y, line in enumerate(input_file.readlines()):
        for x, c in enumerate(line):
            if c == "#":
                INPUT_3D.add((x, y, 0))
                INPUT_4D.add((x, y, 0, 0))


print(f"Part One: {run(INPUT_3D, generate_neighbours_3d)}")
print(f"Part Two: {run(INPUT_4D, generate_neighbours_4d)}")

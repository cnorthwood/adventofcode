#!/usr/bin/env pypy3

from collections import Counter


def neighbours(grid, x, y):
    return sum(1 for location in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)] if location in grid)


def evolve(grid):
    next_grid = set()
    for y in range(5):
        for x in range(5):
            if (x, y) in grid and neighbours(grid, x, y) == 1:
                next_grid.add((x, y))
            elif (x, y) not in grid and 1 <= neighbours(grid, x, y) <= 2:
                next_grid.add((x, y))
    return frozenset(next_grid)


def recursive_neighbours(depth, x, y):
    # consider left neighbour
    if x == 0:
        yield depth + 1, 1, 2
    elif x == 3 and y == 2:
        yield depth - 1, 4, 0
        yield depth - 1, 4, 1
        yield depth - 1, 4, 2
        yield depth - 1, 4, 3
        yield depth - 1, 4, 4
    else:
        yield depth, x - 1, y
    # consider right neighbour
    if x == 4:
        yield depth + 1, 3, 2
    elif x == 1 and y == 2:
        yield depth - 1, 0, 0
        yield depth - 1, 0, 1
        yield depth - 1, 0, 2
        yield depth - 1, 0, 3
        yield depth - 1, 0, 4
    else:
        yield depth, x + 1, y
    # consider above neighbour
    if y == 0:
        yield depth + 1, 2, 1
    elif x == 2 and y == 3:
        yield depth - 1, 0, 4
        yield depth - 1, 1, 4
        yield depth - 1, 2, 4
        yield depth - 1, 3, 4
        yield depth - 1, 4, 4
    else:
        yield depth, x, y - 1
    # consider below neighbour
    if y == 4:
        yield depth + 1, 2, 3
    elif x == 2 and y == 1:
        yield depth - 1, 0, 0
        yield depth - 1, 1, 0
        yield depth - 1, 2, 0
        yield depth - 1, 3, 0
        yield depth - 1, 4, 0
    else:
        yield depth, x, y + 1


def recursive_evolve(grid):
    next_grid = set()
    neighbours_of = Counter()
    for depth, x, y in grid:
        for neighbour in recursive_neighbours(depth, x, y):
            neighbours_of[neighbour] += 1
    for cell, neighbours in neighbours_of.items():
        if neighbours == 1 or cell not in grid and neighbours == 2:
            next_grid.add(cell)
    return frozenset(next_grid)


def biodiversity_rating(grid):
    points = 1
    total = 0
    for y in range(5):
        for x in range(5):
            if (x, y) in grid:
                total += points
            points *= 2
    return total


def find_repeating_grids(start):
    seen = set()
    grid = start
    while grid not in seen:
        seen.add(grid)
        grid = evolve(grid)
    return grid


with open("input.txt") as input_file:
    GRID = frozenset({(x, y) for y, line in enumerate(input_file.readlines()) for x, c in enumerate(line) if c == "#"})

print(f"Part One: {biodiversity_rating(find_repeating_grids(GRID))}")
evolved_grid = frozenset({(0, x, y) for x, y in GRID})
for _ in range(200):
    evolved_grid = recursive_evolve(evolved_grid)
print(f"Part Two: {len(evolved_grid)}")
#!/usr/bin/env pypy3

import sys

OPEN = '.'
TREES = '|'
LUMBERYARD = '#'


def load_grid(filename):
    with open(filename) as input_file:
        return {
            (x, y): c
                for y, line in enumerate(input_file.read().strip().splitlines())
                for x, c in enumerate(line)
        }


def print_grid(grid):
    min_x = min(x for x, y in grid.keys())
    min_y = min(y for x, y in grid.keys())
    max_x = max(x for x, y in grid.keys())
    max_y = max(y for x, y in grid.keys())
    sys.stdout.write('\n\n\n')
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            sys.stdout.write(grid[x, y])
        sys.stdout.write('\n')


def get_adjacent(origin_x, origin_y, grid):
    adjacent = []
    for x, y in {
        (origin_x - 1, origin_y - 1), (origin_x, origin_y - 1), (origin_x + 1, origin_y - 1),
        (origin_x - 1, origin_y),                               (origin_x + 1, origin_y),
        (origin_x - 1, origin_y + 1), (origin_x, origin_y + 1), (origin_x + 1, origin_y + 1),
    }:
        if (x, y) in grid:
            adjacent.append(grid[x, y])
    return adjacent


def iterate(grid):
    next_grid = {}
    for (x, y), current in grid.items():
        if current == OPEN:
            next_grid[x, y] = TREES if sum(1 for c in get_adjacent(x, y, grid) if c == TREES) >= 3 else OPEN
        elif current == TREES:
            next_grid[x, y] = LUMBERYARD if sum(1 for c in get_adjacent(x, y, grid) if c == LUMBERYARD) >= 3 else TREES
        elif current == LUMBERYARD:
            next_grid[x, y] = LUMBERYARD if sum(1 for c in get_adjacent(x, y, grid) if c == LUMBERYARD) >= 1 and sum(1 for c in get_adjacent(x, y, grid) if c == TREES) >= 1 else OPEN
    return next_grid


def run(grid, iterations):
    for _ in range(iterations):
        grid = iterate(grid)
        yield grid


def part_one(grid):
    grid = list(run(grid, 10))[-1]
    return sum(1 for c in grid.values() if c == TREES) * sum(1 for c in grid.values() if c == LUMBERYARD)


# TEST = load_grid('test.txt')
INPUT = load_grid('input.txt')


# assert(part_one(TEST) == 1147)
print("Part One: {}".format(part_one(INPUT)))


def part_two(grid, iterations=1000000000):
    first_grids = list(run(grid, 500))
    reprs = [''.join(g[p] for p in sorted(g)) for g in first_grids]
    for i, g in enumerate(reprs):
        try:
            next_occurrence = reprs.index(g, i + 1)
            loop_starts = i
            loop_length = next_occurrence - i
            break
        except ValueError:
            continue
    else:
        raise Exception()
    grid = first_grids[loop_starts + ((iterations - 1 - loop_starts) % loop_length)]
    return sum(1 for c in grid.values() if c == TREES) * sum(1 for c in grid.values() if c == LUMBERYARD)


print("Part Two: {}".format(part_two(INPUT)))

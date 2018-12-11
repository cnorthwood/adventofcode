#!/usr/bin/env pypy3

from itertools import product

GRID_SIZE = 300


def determine_power(x, y, serial):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    return ((power // 100) % 10) - 5


assert(determine_power(3, 5, 8) == 4)
assert(determine_power(122, 79, 57) == -5)
assert(determine_power(217, 196, 39) == 0)
assert(determine_power(101, 153, 71) == 4)


def grid(serial):
    return {1: {(x, y): determine_power(x, y, serial) for (x, y) in product(range(GRID_SIZE), repeat=2)}}


def populate_grid(grid, n):
    if n - 1 not in grid:
        populate_grid(grid, n - 1)
    grid[n] = {
        (x, y): (grid[n - 1][x, y] + sum(grid[1][x + n - 1, y + right_y] for right_y in range(n)) + sum(grid[1][x + bottom_x, y + n - 1] for bottom_x in range(n - 1)))
            for (x, y) in product(range(GRID_SIZE - n + 1), repeat=2)
    }


def part_one(grid, square_size=3):
    populate_grid(grid, square_size)
    return max(grid[square_size].keys(), key=lambda k: grid[square_size][k])


TEST_GRID = grid(42)
with open('input.txt') as input_file:
    INPUT_GRID = grid(int(input_file.read()))

assert(part_one(TEST_GRID) == (21, 61))
print('Part One: {},{}'.format(*part_one(INPUT_GRID)))


def part_two(grid):
    populate_grid(grid, GRID_SIZE)
    return max(((x, y, size) for size in grid for x, y in grid[size]), key=lambda k: grid[k[2]][k[0], k[1]])


# assert(part_two(grid(18)) == (90, 269, 16))
# assert(part_two(grid(42)) == (232, 251, 12))
print('Part Two: {},{},{}'.format(*part_two(INPUT_GRID)))

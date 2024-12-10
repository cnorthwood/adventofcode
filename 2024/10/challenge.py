#!/usr/bin/env -S python3 -S


def load_input(input_filename):
    grid = {}
    with open(input_filename) as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line.strip()):
                grid[x, y] = int(c)
    return grid


def possible_next_steps(x, y):
    yield x - 1, y
    yield x + 1, y
    yield x, y - 1
    yield x, y + 1


def find_reachable_peaks(grid, x, y, next_height):
    for possible_next_step in possible_next_steps(x, y):
        if possible_next_step in grid and grid[possible_next_step] == next_height:
            if next_height == 9:
                yield possible_next_step
            else:
                yield from find_reachable_peaks(grid, possible_next_step[0], possible_next_step[1], next_height + 1)


def peaks_from_point(grid, x, y):
    if grid[x, y] != 0:
        return 0

    return len(set(find_reachable_peaks(grid, x, y, 1)))


def total_part1(grid):
    return sum(peaks_from_point(grid, x, y) for x, y in grid.keys())


def find_paths(grid, x, y, next_height):
    for possible_next_step in possible_next_steps(x, y):
        if possible_next_step in grid and grid[possible_next_step] == next_height:
            if next_height == 9:
                yield 1
            else:
                yield from find_paths(grid, possible_next_step[0], possible_next_step[1], next_height + 1)


def paths_from_point(grid, x, y):
    if grid[x, y] != 0:
        return 0

    return sum(find_paths(grid, x, y, 1))


def total_part2(grid):
    return sum(paths_from_point(grid, x, y) for x, y in grid.keys())


GRID = load_input("input.txt")
print(f"Part One: {total_part1(GRID)}")
print(f"Part Two: {total_part2(GRID)}")

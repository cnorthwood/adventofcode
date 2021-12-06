#!/usr/bin/env python3

from collections import namedtuple, defaultdict

Line = namedtuple("Line", "start end")
Coord = namedtuple("Coord", "x y")


def load_input(filename):
    lines = []
    with open(filename) as input_file:
        for line in input_file:
            start, end = line.strip().split(" -> ")
            start = Coord(*(int(val) for val in start.split(",")))
            end = Coord(*(int(val) for val in end.split(",")))
            lines.append(Line(start, end))
    return lines


def horiz_or_vert(line):
    return line.start.x == line.end.x or line.start.y == line.end.y


def straight_overlaps(lines, grid):
    for start, end in lines:
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                grid[x, y] += 1


def diag_overlaps(lines, grid):
    for start, end in lines:
        if start.x < end.x and start.y < end.y:
            for x, y in zip(range(start.x, end.x + 1), range(start.y, end.y + 1)):
                grid[x, y] += 1
        elif start.x > end.x and start.y < end.y:
            for x, y in zip(range(start.x, end.x - 1, -1), range(start.y, end.y + 1)):
                grid[x, y] += 1
        elif start.x < end.x and start.y > end.y:
            for x, y in zip(range(start.x, end.x + 1), range(start.y, end.y -1, -1)):
                grid[x, y] += 1
        elif start.x > end.x and start.y > end.y:
            for x, y in zip(range(start.x, end.x - 1, -1), range(start.y, end.y - 1, -1)):
                grid[x, y] += 1


def print_grid(grid):
    for y in range(max([point[1] for point in grid.keys()]) + 1):
        for x in range(max([point[0] for point in grid.keys()]) + 1):
            print(grid[x, y], end="")
        print("")


LINES = load_input("input.txt")
GRID = defaultdict(int)
straight_overlaps((line for line in LINES if horiz_or_vert(line)), GRID)
print(f"Part One: {sum(1 for n in GRID.values() if n >= 2)}")
diag_overlaps((line for line in LINES if not horiz_or_vert(line)), GRID)
print(f"Part Two: {sum(1 for n in GRID.values() if n >= 2)}")

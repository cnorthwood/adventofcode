#!/usr/bin/env pypy3
from collections import defaultdict
from math import inf


def build_tree(line):
    segments = []
    this_segment = []
    c, remaining = line[0], line[1:]
    if c == '^':
        end_char = '$'
    else:
        assert(c == '(')
        end_char = ')'
    while remaining:
        c, remaining = remaining[0], remaining[1:]
        if c == end_char:
            segments.append(this_segment)
            return segments, remaining
        if c == '|':
            segments.append(this_segment)
            this_segment = []
        elif c == '(':
            next_segments, remaining = build_tree(c + remaining)
            this_segment.append(next_segments)
        else:
            this_segment.append(c)


def load_input(filename):
    with open(filename) as input_file:
        segments, remaining = build_tree(input_file.read().strip())
        assert(remaining == '')
        return segments


def build_grid(tree, grid, x=0, y=0, steps=0):
    for segment in tree:
        if isinstance(segment, str):
            if segment == 'N':
                y -= 1
            elif segment == 'S':
                y += 1
            elif segment == 'W':
                x -= 1
            elif segment == 'E':
                x += 1
            steps += 1
            grid[x, y] = min(grid[x, y], steps)
        else:
            build_grid(segment, grid, x, y, steps)


def longest_path(grid):
    return max(grid.values())


def number_of_paths_over(grid, lim=1000):
    return len([1 for v in grid.values() if v >= lim])


GRID = defaultdict(lambda: inf)
build_grid(load_input('input.txt'), GRID)

print("Part One: {}".format(longest_path(GRID)))
print("Part Two: {}".format(number_of_paths_over(GRID)))

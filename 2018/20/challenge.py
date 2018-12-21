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
    grid = defaultdict(lambda: inf)
    edges = {(0, 0, 0)}
    build_grid(segments, grid, edges)
    return grid


def build_grid(tree, grid, edges):
    for segment in tree:
        if isinstance(segment, str):
            if segment == 'N':
                edges = {(x, y - 1, steps + 1) for (x, y, steps) in edges}
            elif segment == 'S':
                edges = {(x, y + 1, steps + 1) for (x, y, steps) in edges}
            elif segment == 'W':
                edges = {(x - 1, y, steps + 1) for (x, y, steps) in edges}
            elif segment == 'E':
                edges = {(x + 1, y, steps + 1) for (x, y, steps) in edges}
            for (x, y, steps) in edges:
                grid[x, y] = min(grid[x, y], steps)
        else:
            next_edges = set()
            for branch in segment:
                next_edges |= build_grid(branch, grid, edges)
            edges = next_edges
    return edges


def longest_path(grid):
    return max(grid.values())


def number_of_paths_over(grid, lim=1000):
    return len([1 for v in grid.values() if v >= lim])


GRID = load_input('input.txt')

print("Part One: {}".format(longest_path(GRID)))
print("Part Two: {}".format(number_of_paths_over(GRID)))

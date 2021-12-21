#!/usr/bin/env pypy3

from collections import defaultdict
from heapq import heappush, heappop
from math import inf


def load_map(filename):
    with open(filename) as input_file:
        return {(x, y): int(c) for y, line in enumerate(input_file) for x, c in enumerate(line.strip())}


def clamp_risk(risk):
    while risk > 9:
        risk -= 9
    return risk


def expand_map(map):
    expanded_map = {}
    x_size = max(x for x, y in map.keys()) + 1
    y_size = max(y for x, y in map.keys()) + 1
    for repeat_y in range(5):
        for repeat_x in range(5):
            corner_x, corner_y = (repeat_x * x_size), (repeat_y * y_size)
            for (x, y), risk in map.items():
                expanded_map[corner_x + x, corner_y + y] = clamp_risk(risk + repeat_x + repeat_y)
    return expanded_map


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return reversed(total_path)


def a_star_search(map):
    start = 0, 0
    max_x = max(x for x, y in map.keys())
    max_y = max(y for x, y in map.keys())
    goal = max_x, max_y

    def h(coord):
        return abs(coord[0] - max_x) + abs(coord[1] - max_y)

    def neighbours(coord):
        x, y = coord
        if (x - 1, y) in map:
            yield (x - 1, y)
        if (x + 1, y) in map:
            yield (x + 1, y)
        if (x, y - 1) in map:
            yield (x, y - 1)
        if (x, y + 1) in map:
            yield (x, y + 1)


    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = defaultdict(lambda: inf)
    g_score[start] = 0

    f_score = defaultdict(lambda: inf)
    f_score[start] = h((0, 0))

    while open_set:
        _, current = heappop(open_set)
        if current == goal:
            return sum(map[coord] for coord in reconstruct_path(came_from, current)) - map[start]

        for neighbour in neighbours(current):
            tentative_g_score = g_score[current] + map[neighbour]
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + h(neighbour)
                if neighbour not in open_set:
                    heappush(open_set, (f_score[neighbour], neighbour))

    return None


INITIAL_MAP = load_map("input.txt")
print(f"Part One: {a_star_search(INITIAL_MAP)}")
print(f"Part Two: {a_star_search(expand_map(INITIAL_MAP))}")

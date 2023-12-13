#!/usr/bin/env python3

from collections import deque
from math import inf


def load_input(filename):
    connections = {}
    start = None
    with open(filename) as input_file:
        for y, line in enumerate(input_file):
            for x, c in enumerate(line.strip()):
                if c == "S":
                    start = (x, y)
                elif c == "|":
                    connections[x, y] = {(x, y - 1), (x, y + 1)}
                elif c == "-":
                    connections[x, y] = {(x - 1, y), (x + 1, y)}
                elif c == "L":
                    connections[x, y] = {(x, y - 1), (x + 1, y)}
                elif c == "J":
                    connections[x, y] = {(x, y - 1), (x - 1, y)}
                elif c == "7":
                    connections[x, y] = {(x, y + 1), (x - 1, y)}
                elif c == "F":
                    connections[x, y] = {(x, y + 1), (x + 1, y)}
                elif c == ".":
                    pass
                else:
                    raise ValueError(f"unknown map character: {c}")

    start_x, start_y = start
    if start in connections[start_x, start_y - 1] and start in connections[start_x, start_y + 1]:
        # |
        connections[start] = {(start_x, start_y - 1), (start_x, start_y + 1)}
    elif start in connections[start_x - 1, start_y] and start in connections[start_x + 1, start_y]:
        # -
        connections[start] = {(start_x - 1, start_y), (start_x + 1, start_y)}
    elif start in connections[start_x, start_y - 1] and start in connections[start_x + 1, start_y]:
        # L
        connections[start] = {(start_x, start_y - 1), (start_x + 1, start_y)}
    elif start in connections[start_x, start_y - 1] and start in connections[start_x - 1, start_y]:
        # J
        connections[start] = {(start_x, start_y - 1), (start_x - 1, start_y)}
    elif start in connections[start_x, start_y + 1] and start in connections[start_x - 1, start_y]:
        # 7
        connections[start] = {(start_x, start_y + 1), (start_x - 1, start_y)}
    elif start in connections[start_x, start_y + 1] and start in connections[start_x + 1, start_y]:
        # F
        connections[start] = {(start_x, start_y + 1), (start_x + 1, start_y)}
    else:
        raise ValueError("Couldn't figure out what tile type S is")

    return start, connections


def populate_distances(start, connections):
    distances = {}
    q = deque([(start, 0)])
    while len(q):
        coord, distance = q.popleft()
        if distance < distances.get(coord, inf):
            distances[coord] = distance
            for neighbour in connections[coord]:
                q.append((neighbour, distance + 1))
    return distances


def loop_points(start, connections):
    current = start
    points = []
    while current != start or len(points) == 0:
        next_point = (connections[current] - set(points[-1:])).pop()
        points.append(current)
        current = next_point
    return points


# Shoelace formula: https://codereview.stackexchange.com/questions/88010/area-of-an-irregular-polygon
def polygon_area(points):
    area = 0
    q = points[-1]
    for p in points:
        area += p[0] * q[1] - p[1] * q[0]
        q = p
    return area / 2


# picks theorem - https://advent-of-code.xavd.id/writeups/2023/day/10/
def num_interior_points(area, points):
    return int(abs(area) - 0.5 * len(points) + 1)


START, CONNECTIONS = load_input("input.txt")
LOOP_POINTS = loop_points(START, CONNECTIONS)
print(f"Part One: {max(populate_distances(START, CONNECTIONS).values())}")
print(f"Part Two: {num_interior_points(polygon_area(LOOP_POINTS), LOOP_POINTS)}")

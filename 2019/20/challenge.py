#!/usr/bin/env pypy3

from collections import defaultdict, deque
from string import ascii_uppercase


def build_graph(map):
    graph = defaultdict(set)
    portals = defaultdict(set)
    for (x, y), c in map.items():
        if c != ".":
            continue
        if map.get((x - 1, y), " ") == ".":
            graph[x, y].add((x - 1, y))
            graph[x - 1, y].add((x, y))
        if map.get((x + 1, y), " ") == ".":
            graph[x, y].add((x + 1, y))
            graph[x + 1, y].add((x, y))
        if map.get((x, y - 1), " ") == ".":
            graph[x, y].add((x, y - 1))
            graph[x, y - 1].add((x, y))
        if map.get((x, y + 1), " ") == ".":
            graph[x, y].add((x, y + 1))
            graph[x, y + 1].add((x, y))
        if map.get((x - 1, y), " ") in ascii_uppercase and map.get((x - 2, y), " ") in ascii_uppercase:
            portal = map[x - 2, y] + map[x - 1, y]
            portals[portal].add((x, y))
            if portal not in {"AA", "ZZ"}:
                graph[x, y].add(portal)
        if map.get((x + 1, y), " ") in ascii_uppercase and map.get((x + 2, y), " ") in ascii_uppercase:
            portal = map[x + 1, y] + map[x + 2, y]
            portals[portal].add((x, y))
            if portal not in {"AA", "ZZ"}:
                graph[x, y].add(portal)
        if map.get((x, y - 2), " ") in ascii_uppercase and map.get((x, y - 1), " ") in ascii_uppercase:
            portal = map[x, y - 2] + map[x, y - 1]
            portals[portal].add((x, y))
            if portal not in {"AA", "ZZ"}:
                graph[x, y].add(portal)
        if map.get((x, y + 1), " ") in ascii_uppercase and map.get((x, y + 2), " ") in ascii_uppercase:
            portal = map[x, y + 1] + map[x, y + 2]
            portals[portal].add((x, y))
            if portal not in {"AA", "ZZ"}:
                graph[x, y].add(portal)
    return portals["AA"].pop(), graph, portals, portals["ZZ"].pop()


def find_path(start, graph, portals, end):
    queue = deque()
    queue.append((start, 0, frozenset()))
    while queue:
        pos, steps, visited = queue.popleft()
        if pos == end:
            return steps
        for next_pos in graph[pos]:
            if next_pos in portals:
                next_pos = next(portal_pos for portal_pos in portals[next_pos] if portal_pos != pos)
            if next_pos in visited:
                continue
            queue.append((next_pos, steps + 1, frozenset(visited | {next_pos})))


def find_path_with_depth(start, graph, portals, end):
    queue = deque()
    queue.append((start, 0, 0, frozenset()))
    min_x = min(pos[0] for pos in graph.keys())
    max_x = max(pos[0] for pos in graph.keys())
    min_y = min(pos[1] for pos in graph.keys())
    max_y = max(pos[1] for pos in graph.keys())
    while queue:
        pos, steps, depth, visited = queue.popleft()
        if pos == end and depth == 0:
            return steps
        for next_pos in graph[pos]:
            next_depth = depth
            if next_pos in portals:
                next_pos = next(portal_pos for portal_pos in portals[next_pos] if portal_pos != pos)
                if pos[0] == min_x or pos[0] == max_x or pos[1] == min_y or pos[1] == max_y:
                    if depth == 0:
                        continue
                    else:
                        next_depth -= 1
                else:
                    next_depth += 1
            # Assumption alert about max depth...
            if (next_depth, next_pos) in visited or next_depth > 30:
                continue
            queue.append((next_pos, steps + 1, next_depth, frozenset(visited | {(next_depth, next_pos)})))


with open("input.txt") as input_file:
    MAP = {(x, y): c for y, line in enumerate(input_file) for x, c in enumerate(line)}
START, GRAPH, PORTALS, END = build_graph(MAP)
print(f"Part One: {find_path(START, GRAPH, PORTALS, END)}")
print(f"Part Two: {find_path_with_depth(START, GRAPH, PORTALS, END)}")
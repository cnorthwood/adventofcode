#!/usr/bin/env pypy3

from collections import defaultdict, deque
from heapq import heapify, heappop, heappush
from itertools import permutations
from math import inf
from string import ascii_lowercase, ascii_uppercase


def parse_map(input):
    cave = defaultdict(lambda: "#")
    for y, line in enumerate(input.splitlines(keepends=False)):
        for x, c in enumerate(line):
            cave[x, y] = c
    keys = {}
    doors = {}
    moves = {}
    start = None
    for (x, y), c in cave.items():
        if c == "#":
            continue
        elif c == "@":
            start = x, y
        elif c in ascii_lowercase:
            keys[x, y] = c
        elif c in ascii_uppercase:
            doors[x, y] = c
        moves[x, y] = []
        if cave[x - 1, y] != "#":
            moves[x, y].append((x - 1, y))
        if cave[x + 1, y] != "#":
            moves[x, y].append((x + 1, y))
        if cave[x, y - 1] != "#":
            moves[x, y].append((x, y - 1))
        if cave[x, y + 1] != "#":
            moves[x, y].append((x, y + 1))
    return start, moves, keys, doors


def find_path(moves, doors, a, b):
    queue = deque([(a, frozenset(), 0, frozenset())])
    while queue:
        pos, keys_needed, steps, visited = queue.popleft()
        if pos == b:
            return keys_needed, steps
        for next_pos in moves[pos]:
            if next_pos in visited:
                continue
            queue.append(
                (
                    next_pos,
                    frozenset(keys_needed | ({doors[next_pos].lower()} if next_pos in doors else set())),
                    steps + 1,
                    frozenset(visited | {pos})
                )
            )
    return None


def paths(start, moves, keys, doors):
    distances = defaultdict(dict)
    for a, b in permutations([start] + list(keys.keys()), r=2):
        if b in distances[a]:
            continue
        distances[a][b] = distances[b][a] = find_path(moves, doors, a, b)
    return distances


def find_shortest(start, paths, keys):
    queue = [(0, start, frozenset())]
    min_steps_for_keys = {}
    heapify(queue)
    while queue:
        steps, pos, keys_obtained = heappop(queue)
        if len(keys_obtained) == len(keys):
            return steps
        for next_pos, (keys_needed, next_steps) in paths[pos].items():
            if next_pos not in keys or keys[next_pos] in keys_obtained or not all(key_needed in keys_obtained for key_needed in keys_needed):
                continue
            next_keys_obtained = frozenset(keys_obtained | {keys[next_pos]})
            if steps + next_steps < min_steps_for_keys.get((next_pos, next_keys_obtained), inf):
                min_steps_for_keys[(next_pos, next_keys_obtained)] = steps + next_steps
                heappush(queue, (
                    steps + next_steps,
                    next_pos,
                    frozenset(keys_obtained | {keys[next_pos]}),
                ))


with open("input.txt") as input_file:
    START, MOVES, KEYS, DOORS = parse_map(input_file.read())
PATHS = paths(START, MOVES, KEYS, DOORS)

print(f"Part One: {find_shortest(START, PATHS, KEYS)}")

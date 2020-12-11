#!/usr/bin/env python3

def load_input():
    seats = {}
    with open("input.txt") as input_file:
        for y, line in enumerate(input_file.readlines()):
            for x, c in enumerate(line.strip()):
                if c == "L":
                    seats[x, y] = False
    return seats


def compute_adjacency_map(xys):
    adjacencies = {}
    for x, y in xys:
        adjacencies[x, y] = set()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if MIN_X <= x + dx <= MAX_X and MIN_Y <= y + dy <= MAX_Y and (x + dx, y + dy) in xys and (x + dx, y + dy) != (x, y):
                    adjacencies[x, y].add((x + dx, y + dy))
    return adjacencies


def find_next_visible_seat(origin_x, origin_y, dx, dy, seats):
    x = origin_x + dx
    y = origin_y + dy
    while MIN_X <= x <= MAX_X and MIN_Y <= y <= MAX_Y:
        if (x, y) in seats:
            return (x, y)
        else:
            x += dx
            y += dy
    return None


def compute_visibility_map(xys):
    adjacencies = {}
    for x, y in xys:
        adjacencies[x, y] = set()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (x + dx, y + dy) != (x, y):
                    visible_xy = find_next_visible_seat(x, y, dx, dy, xys)
                    if visible_xy is not None:
                        adjacencies[x, y].add(visible_xy)
    return adjacencies


def apply_rules(seats, adjacency_map, occupied_limit):
    next_generation = {}
    for (x, y), occupied in seats.items():
        occupied_adjacent_seats = sum(1 for xy in adjacency_map[x, y] if seats[xy])
        if not occupied and occupied_adjacent_seats == 0:
            next_generation[x, y] = True
        elif occupied and occupied_adjacent_seats >= occupied_limit:
            next_generation[x, y] = False
        else:
            next_generation[x, y] = occupied
    return next_generation


def find_stability(seats, adjacency_map, occupied_limit):
    last_seen = frozenset()
    while True:
        seats = apply_rules(seats, adjacency_map, occupied_limit)
        occupied_seats = frozenset(xy for xy, occupied in seats.items() if occupied)
        if occupied_seats == last_seen:
            return len(occupied_seats)
        last_seen = occupied_seats


SEATS = load_input()
MIN_X = min(x for x, y in SEATS.keys())
MIN_Y = min(y for x, y in SEATS.keys())
MAX_X = max(x for x, y in SEATS.keys())
MAX_Y = max(y for x, y in SEATS.keys())
ADJACENT_SEATS = compute_adjacency_map(SEATS.keys())
VISIBLE_SEATS = compute_visibility_map(SEATS.keys())
print(f"Part One: {find_stability(SEATS, ADJACENT_SEATS, 4)}")
print(f"Part Two: {find_stability(SEATS, VISIBLE_SEATS, 5)}")

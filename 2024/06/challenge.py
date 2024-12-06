#!/usr/bin/env pypy3 -S

from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def load_map(input_filename):
    max_y = 0
    max_x = 0
    start_pos = None
    obstacles = set()
    with open(input_filename) as input_file:
        for y, line in enumerate(input_file):
            max_y = max(y, max_y)
            for x, c in enumerate(line):
                if c == "#":
                    obstacles.add((x, y))
                elif c == ".":
                    max_x = max(x, max_x)
                elif c == "^":
                    start_pos = (x, y), Direction.UP
    return start_pos, obstacles, (max_x, max_y)


def turn(pos):
    if pos[1] == Direction.UP:
        return pos[0], Direction.RIGHT
    elif pos[1] == Direction.RIGHT:
        return pos[0], Direction.DOWN
    elif pos[1] == Direction.DOWN:
        return pos[0], Direction.LEFT
    elif pos[1] == Direction.LEFT:
        return pos[0], Direction.UP


def next_pos(pos, obstacles):
    forward_pos = pos[0][0] + pos[1].value[0], pos[0][1] + pos[1].value[1]
    if forward_pos in obstacles:
        return turn(pos)
    else:
        return forward_pos, pos[1]


def in_grid(pos, grid_limits):
    return 0 <= pos[0][0] <= grid_limits[0] and 0 <= pos[0][1] <= grid_limits[1]


def covered_steps(pos, obstacles, grid_limits):
    visited = set()
    while in_grid(pos, grid_limits):
        visited.add(pos[0])
        pos = next_pos(pos, obstacles)
    return visited


def will_loop(pos, obstacles, grid_limits):
    visited = set()
    while pos not in visited:
        visited.add(pos)
        pos = next_pos(pos, obstacles)
        if not in_grid(pos, grid_limits):
            return False
    return True


def possible_obstacle_placements(start_pos, obstacles, places_to_try, grid_limits):
    looping_obstacles = set()
    places_to_try = {pos for pos in places_to_try if pos != start_pos[0]}
    for place_to_try in places_to_try:
        if will_loop(start_pos, obstacles | {place_to_try}, grid_limits):
            looping_obstacles.add(place_to_try)
    return len(looping_obstacles)


START_POS, OBSTACLES, GRID_LIMITS = load_map("input.txt")
VISITED_STEPS = covered_steps(START_POS, OBSTACLES, GRID_LIMITS)
print(f"Part One: {len(VISITED_STEPS)}")
print(f"Part Two: {possible_obstacle_placements(START_POS, OBSTACLES, VISITED_STEPS, GRID_LIMITS)}")

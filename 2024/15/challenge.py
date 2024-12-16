#!/usr/bin/env -S python3 -S

from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


INPUT_DIRECTIONS = {
    "^": Direction.UP,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
    ">": Direction.RIGHT,
}

WALL = "#"
BOX = "O"
EMPTY = "."


def load_input(input_filename):
    grid = {}
    moves = []
    start_pos = None
    with open(input_filename) as input_file:
        for y, line in enumerate(input_file):
            line = line.strip()
            if not line:
                break
            for x, c in enumerate(line):
                if c == "@":
                    start_pos = x, y
                    c = EMPTY
                grid[x, y] = c

        for line in input_file:
            moves.extend(line.strip())

    return start_pos, grid, [INPUT_DIRECTIONS[move] for move in moves]


def apply_direction(pos, direction):
    return pos[0] + direction.value[0], pos[1] + direction.value[1]


def move(pos, grid, direction):
    next_pos = apply_direction(pos, direction)
    if grid[next_pos] == WALL:
        return False
    elif grid[next_pos] == EMPTY or move(next_pos, grid, direction):
        grid[next_pos] = grid[pos]
        grid[pos] = EMPTY
        return True
    else:
        return False


def boxes_gps(grid):
    return sum(x + y * 100 for (x, y), c in grid.items() if c == BOX)


def process_instructions(pos, grid, instructions):
    grid = grid.copy()
    for instruction in instructions:
        if move(pos, grid, instruction):
            pos = apply_direction(pos, instruction)
    return grid


print(f"Part One: {boxes_gps(process_instructions(*load_input('input.txt')))}")

#!/usr/bin/env -S pypy3 -S

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
BOX_LEFT = "["
BOX_RIGHT = "]"


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


def part2_grid(start_pos, grid):
    doubled_grid = {}
    for (x, y), c in grid.items():
        if c != BOX:
            doubled_grid[x * 2, y] = c
            doubled_grid[x * 2 + 1, y] = c
        else:
            doubled_grid[x * 2, y] = BOX_LEFT
            doubled_grid[x * 2 + 1, y] = BOX_RIGHT
    return (start_pos[0] * 2, start_pos[1]), doubled_grid


def apply_direction(pos, direction):
    return pos[0] + direction.value[0], pos[1] + direction.value[1]


def atomic_move(pos, grid, direction):
    next_pos = apply_direction(pos, direction)
    if grid[next_pos] == WALL:
        return False
    elif grid[next_pos] == EMPTY or atomic_move(next_pos, grid, direction):
        grid[next_pos] = grid[pos]
        grid[pos] = EMPTY
        return True
    else:
        return False


def check_width_aware_move(pos, grid, direction):
    next_pos = apply_direction(pos, direction)
    if grid[next_pos] == WALL:
        return False
    elif grid[next_pos] == EMPTY:
        return True
    # need to move as a pair if we're moving up/down
    elif (direction == Direction.UP or direction == Direction.DOWN) and grid[next_pos] == BOX_LEFT:
        return check_width_aware_move(next_pos, grid, direction) and check_width_aware_move(apply_direction(next_pos, Direction.RIGHT), grid, direction)
    elif (direction == Direction.UP or direction == Direction.DOWN) and grid[next_pos] == BOX_RIGHT:
        return check_width_aware_move(next_pos, grid, direction) and check_width_aware_move(apply_direction(next_pos, Direction.LEFT), grid, direction)
    else:
        return check_width_aware_move(next_pos, grid, direction)


def unsafe_width_aware_move(pos, grid, direction):
    next_pos = apply_direction(pos, direction)

    # the next location is the wall, so we can't move
    if grid[next_pos] == WALL:
        return

    # next location is empty, so we just move into it
    elif grid[next_pos] == EMPTY:
        grid[next_pos] = grid[pos]
        grid[pos] = EMPTY

    # next location is a box, and we're moving up and down so this might need to chain with the other half of the box
    elif (direction == Direction.UP or direction == Direction.DOWN) and grid[next_pos] == BOX_LEFT:
        unsafe_width_aware_move(next_pos, grid, direction)
        unsafe_width_aware_move(apply_direction(next_pos, Direction.RIGHT), grid, direction)
        grid[next_pos] = grid[pos]
        grid[pos] = EMPTY
    elif (direction == Direction.UP or direction == Direction.DOWN) and grid[next_pos] == BOX_RIGHT:
        unsafe_width_aware_move(next_pos, grid, direction)
        unsafe_width_aware_move(apply_direction(next_pos, Direction.LEFT), grid, direction)
        grid[next_pos] = grid[pos]
        grid[pos] = EMPTY
    # next location is a box, but we're moving left/right so this is a straight forward chain
    else:
        unsafe_width_aware_move(next_pos, grid, direction)
        grid[next_pos] = grid[pos]
        grid[pos] = EMPTY


def width_aware_move(pos, grid, direction):
    if not check_width_aware_move(pos, grid, direction):
        return False

    unsafe_width_aware_move(pos, grid, direction)
    return True


def boxes_gps(grid):
    return sum(x + y * 100 for (x, y), c in grid.items() if c == BOX or c == BOX_LEFT)


def process_instructions(pos, grid, instructions, move_func):
    grid = grid.copy()
    for instruction in instructions:
        # visualise(pos, grid)
        if move_func(pos, grid, instruction):
            pos = apply_direction(pos, instruction)
    return grid


def visualise(pos, grid):
    max_x = max(x for x, y in grid.keys())
    max_y = max(y for x, y in grid.keys())
    print()
    for y in range(max_y + 1):
        print("".join("@" if (x, y) == pos else grid[x, y] for x in range(max_x + 1)))
    print()


if __name__ == "__main__":
    START_POS, GRID, INSTRUCTIONS = load_input("input.txt")
    print(f"Part One: {boxes_gps(process_instructions(START_POS, GRID, INSTRUCTIONS, move_func=atomic_move))}")
    print(f"Part Two: {boxes_gps(process_instructions(*part2_grid(START_POS, GRID), INSTRUCTIONS, move_func=width_aware_move))}")

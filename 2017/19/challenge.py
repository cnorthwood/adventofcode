#!/usr/bin/env pypy3


def build_grid(input):
    return [[c for c in line] for line in input.splitlines()]


def find_start(grid):
    y = 0
    for x, start_loc in enumerate(grid[0]):
        if start_loc != ' ':
            break
    return x, y


def change_direction(location, current_direction, grid):
    x, y = location
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]
    for (direction_x, direction_y) in directions:
        next_x = x + direction_x
        next_y = y + direction_y
        if (direction_x * -1, direction_y * -1) == current_direction:
            continue
        if next_y < 0 or next_y >= len(grid) or next_x < 0 or next_x >= len(grid[next_y]):
            continue
        if grid[next_y][next_x] != ' ':
            return (direction_x, direction_y)


def path_find(grid):
    x, y = find_start(grid)
    direction_x, direction_y = (0, 1)
    acc = []
    while True:
        if grid[y][x] == ' ':
            return ''.join(acc)

        if grid[y][x] == '+':
            direction_x, direction_y = change_direction((x, y), (direction_x, direction_y), grid)

        if grid[y][x] not in ('|', '-', '+'):
            acc.append(grid[y][x])

        x += direction_x
        y += direction_y


TEST_GRID = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
"""

assert path_find(build_grid(TEST_GRID)) == 'ABCDEF'

with open('input.txt') as INPUT:
    GRID = build_grid(INPUT.read())

print("Part One:", path_find(GRID))

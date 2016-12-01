#!/usr/bin/env python

INPUT = "L4, L1, R4, R1, R1, L3, R5, L5, L2, L3, R2, R1, L4, R5, R4, L2, R1, R3, L5, R1, L3, L2, R5, L4, L5, R1, R2, L1, R5, L3, R2, R2, L1, R5, R2, L1, L1, R2, L1, R1, L2, L2, R4, R3, R2, L3, L188, L3, R2, R54, R1, R1, L2, L4, L3, L2, R3, L1, L1, R3, R5, L1, R5, L1, L1, R2, R4, R4, L5, L4, L1, R2, R4, R5, L2, L3, R5, L5, R1, R5, L2, R4, L2, L1, R4, R3, R4, L4, R3, L4, R78, R2, L3, R188, R2, R3, L2, R2, R3, R1, R5, R1, L1, L1, R4, R2, R1, R5, L1, R4, L4, R2, R5, L2, L5, R4, L3, L2, R1, R1, L5, L4, R1, L5, L1, L5, L1, L4, L3, L5, R4, R5, R2, L5, R5, R5, R4, R2, L1, L2, R3, R5, R5, R5, L2, L1, R4, R3, R1, L4, L2, L3, R2, L3, L5, L2, L2, L1, L2, R5, L2, L2, L3, L1, R1, L4, R2, L4, R3, R5, R3, R4, R1, R5, L3, L5, L5, L3, L2, L1, R3, L4, R3, R2, L1, R3, R1, L2, R4, L3, L3, L3, L1, L2"

def parse_input(input):
    for instruction in input.split(', '):
        yield instruction[0], int(instruction[1:])

TURN_RESULTS = {
    'N': {'L': 'W', 'R': 'E'},
    'S': {'L': 'E', 'R': 'W'},
    'W': {'L': 'S', 'R': 'N'},
    'E': {'L': 'N', 'R': 'S'},
}

VISITED_BLOCKS = {0, 0}


def visit(x, y):
    print x, y
    if (x, y) in VISITED_BLOCKS:
        return True
    else:
        VISITED_BLOCKS.add((x, y))


def get_first_block_visited_twice_distance():
    x = 0
    y = 0
    d = 'N'
    for turn, walk in parse_input(INPUT):
        d = TURN_RESULTS[d][turn]
        if d == 'N':
            for new_y in range(y, y + walk):
                if visit(x, new_y + 1):
                    return x + new_y + 1
            y += walk
        elif d == 'S':
            for new_y in range(y - walk, y):
                if visit(x, new_y):
                    return x + new_y
            y -= walk
        elif d == 'E':
            for new_x in range(x, x + walk):
                if visit(new_x + 1, y):
                    return new_x + 1 + y
            x += walk
        elif d == 'W':
            for new_x in range(x - walk, x):
                if visit(new_x, y):
                    return new_x + y
            x -= walk

print get_first_block_visited_twice_distance()

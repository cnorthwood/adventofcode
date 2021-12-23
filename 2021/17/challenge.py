#!/usr/bin/env pypy3

import re


def load_input(filename):
    with open(filename) as input_file:
        match = re.match(r'target area: x=(?P<min_x>-?\d+)..(?P<max_x>-?\d+), y=(?P<min_y>-?\d+)..(?P<max_y>-?\d+)', input_file.read())
        return (int(match.group("min_x")), int(match.group("max_x"))), (int(match.group("min_y")), int(match.group("max_y")))


def in_area(pos, bounds):
    pos_x, pos_y = pos
    (min_x, max_x), (min_y, max_y) = bounds
    return min_x <= pos_x <= max_x and min_y <= pos_y <= max_y


def unrecoverable(pos, bounds):
    pos_x, pos_y = pos
    (min_x, max_x), (min_y, max_y) = bounds
    return pos_x > max_x or pos_y < min_y


def step(pos, vel):
    pos_x, pos_y = pos
    vel_x, vel_y = vel
    return (pos_x + vel_x, pos_y + vel_y), (vel_x - 1 if vel_x > 0 else vel_x + 1 if vel_x < 0 else 0, vel_y - 1)


def will_vel_satisfy(vel, bounds):
    pos = 0, 0
    highest_y = 0
    while not unrecoverable(pos, bounds):
        pos, vel = step(pos, vel)
        highest_y = max(highest_y, pos[1])
        if in_area(pos, bounds):
            return highest_y
    else:
        return None


def calculate(bounds):
    valid = 0
    max_y = 0
    for y in range(BOUNDS[1][0], BOUNDS[0][1]):
        for x in range(bounds[0][1] + 1):
            y_reached = will_vel_satisfy((x, y), bounds)
            if y_reached is not None:
                max_y = max(max_y, y_reached)
                valid += 1
    return max_y, valid


BOUNDS = load_input("input.txt")
part_one, part_two = calculate(BOUNDS)
print(f"Part One: {part_one}")
print(f"Part Two: {part_two}")

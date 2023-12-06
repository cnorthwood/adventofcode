#!/usr/bin/env python3

from math import prod


def parse_input(filename):
    vals = {}
    with open(filename) as input_file:
        for line in input_file.readlines():
            head, tail = line.split(":")
            vals[head] = [int(v) for v in tail.split()]
    return list(zip(vals["Time"], vals["Distance"]))


def ways_to_win(duration, record):
    wins = 0
    for hold_t in range(1, duration):
        speed = hold_t
        run_t = duration - hold_t
        if speed * run_t > record:
            wins += 1
    return wins


assert(ways_to_win(7, 9) == 4)

INPUT = parse_input("input.txt")
print(f"Part One: {prod(ways_to_win(duration, record) for duration, record in INPUT)}")
print(f"Part Two: {ways_to_win(int(''.join(str(t) for t, _ in INPUT)), int(''.join(str(d) for _, d in INPUT)))}")

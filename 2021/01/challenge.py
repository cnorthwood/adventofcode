#!/usr/bin/env python3

with open("input.txt") as input_file:
    INPUT = [int(line) for line in input_file]


def windows(measurements):
    for a, b, c in zip(measurements, measurements[1:], measurements[2:]):
        yield a + b + c


WINDOWS = list(windows(INPUT))

print(f"Part One: {sum(1 for previous, current in zip(INPUT, INPUT[1:]) if current > previous)}")
print(f"Part Two: {sum(1 for previous, current in zip(WINDOWS, WINDOWS[1:]) if current > previous)}")

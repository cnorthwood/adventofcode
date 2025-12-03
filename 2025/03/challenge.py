#!/usr/bin/env python3

from itertools import combinations


def load_input(filename):
    with open(filename) as input_file:
        return [list(line.strip()) for line in input_file.readlines()]


def max_joltage(battery_bank, batteries):
    return max(int("".join(batteries)) for batteries in combinations(battery_bank, batteries))


INPUT = load_input("input.txt")
print(f"Part One: {sum(max_joltage(battery_bank, batteries=2) for battery_bank in INPUT)}")
# print(f"Part Two: {sum(max_joltage(battery_bank, batteries=12) for battery_bank in INPUT)}")

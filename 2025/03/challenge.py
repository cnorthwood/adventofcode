#!/usr/bin/env python3

from itertools import combinations


def load_input(filename):
    with open(filename) as input_file:
        return [[int(c) for c in line.strip()] for line in input_file.readlines()]


def max_joltage(battery_bank, batteries):
    selected = []
    current_index = -1
    while len(selected) < batteries:
        if batteries - len(selected) == 1:
            window = battery_bank[current_index + 1:]
        else:
            window = battery_bank[current_index + 1:1-batteries + len(selected)]
        next_highest = max(battery for battery in window)
        selected.append(str(next_highest))
        current_index = window.index(next_highest) + current_index + 1
    return int("".join(selected))

INPUT = load_input("input.txt")
print(f"Part One: {sum(max_joltage(battery_bank, batteries=2) for battery_bank in INPUT)}")
print(f"Part Two: {sum(max_joltage(battery_bank, batteries=12) for battery_bank in INPUT)}")

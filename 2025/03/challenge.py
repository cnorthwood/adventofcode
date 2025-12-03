#!/usr/bin/env python3


def load_input(filename):
    with open(filename) as input_file:
        return [[int(c) for c in line.strip()] for line in input_file.readlines()]


def max_joltage(battery_bank, batteries):
    selected = []
    window_start = 0

    while len(selected) < batteries:
        window_end = 1 - batteries + len(selected)
        window = battery_bank[window_start:None if window_end == 0 else window_end]

        next_highest = max(window)

        selected.append(str(next_highest))
        window_start = window_start + window.index(next_highest) + 1

    return int("".join(selected))

INPUT = load_input("input.txt")
print(f"Part One: {sum(max_joltage(battery_bank, batteries=2) for battery_bank in INPUT)}")
print(f"Part Two: {sum(max_joltage(battery_bank, batteries=12) for battery_bank in INPUT)}")

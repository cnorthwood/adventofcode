#!/usr/bin/env python3


def load_turns(filename):
    with open(filename) as input_file:
        return [int(line[1:].strip()) * (-1 if line[0] == "L" else 1) for line in input_file.readlines()]


def part_one(turns):
    zeros = 0
    dial = 50
    for turn in turns:
        dial = (dial + turn) % 100
        if dial == 0:
            zeros += 1
    return zeros


def part_two(turns):
    zeros = 0
    dial = 50
    for turn in turns:
        started_on_zero = dial == 0
        dial += turn
        if started_on_zero and dial < 0:
            zeros -= 1
        while dial < 0:
            dial += 100
            zeros += 1
        while dial >= 100:
            dial -= 100
            if dial > 0:
                zeros += 1
        if dial == 0:
            zeros += 1
    return zeros


# print(part_two(load_turns("test.txt")))

TURNS = load_turns("input.txt")
print(f"Part One: {part_one(TURNS)}")
print(f"Part Two: {part_two(TURNS)}")

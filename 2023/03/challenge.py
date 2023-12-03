#!/usr/bin/env python3

from math import prod
import re


def load_map(filename):
    numbers = []
    symbol_coords = set()
    gear_coords = set()
    with open(filename) as input_file:
        for y, line in enumerate(input_file.readlines()):
            for match in re.finditer(r"\d+", line.strip()):
                numbers.append((int(match.group()), {(x, y) for x in range(match.start(), match.end())}))
            for x, c in enumerate(line.strip()):
                if c.isdigit() or c == ".":
                    continue
                if c == "*":
                    gear_coords.add((x, y))
                symbol_coords.add((x, y))
    return numbers, symbol_coords, gear_coords


def adjacent(x, y):
    return {
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    }


def is_part_number(number_coords, symbol_coords):
    return any(coord in symbol_coords for number_coord in number_coords for coord in adjacent(*number_coord))


def gear_ratio(gear_coord, number_coords):
    adjacent_numbers = []
    for part_number, coords in number_coords:
        if any(adjacent_coord in coords for adjacent_coord in adjacent(*gear_coord)):
            adjacent_numbers.append(part_number)
    if len(adjacent_numbers) != 2:
        return 0
    return prod(adjacent_numbers)


NUMBER_MAP, SYMBOL_MAP, GEAR_MAP = load_map("input.txt")
print(f"Part One: {sum(part_number for part_number, number_coords in NUMBER_MAP if is_part_number(number_coords, SYMBOL_MAP))}")
print(f"Part Two: {sum(gear_ratio(gear_coord, NUMBER_MAP) for gear_coord in GEAR_MAP)}")
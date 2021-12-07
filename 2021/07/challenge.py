#!/usr/bin/env python3
from functools import lru_cache

with open("input.txt") as input_file:
    INITIAL_POSITIONS = [int(val) for val in input_file.read().strip().split(",")]


def linear_fuel_consumption(crabs, pos):
    return sum(abs(crab - pos) for crab in crabs)


def triangle_number(n):
    return n * (n + 1) // 2


def crab_fuel_consumption(crabs, pos):
    return sum(triangle_number(abs(crab - pos)) for crab in crabs)


print(f"Part One: {min(linear_fuel_consumption(INITIAL_POSITIONS, pos) for pos in range(min(INITIAL_POSITIONS), max(INITIAL_POSITIONS)))}")
print(f"Part Two: {min(crab_fuel_consumption(INITIAL_POSITIONS, pos) for pos in range(min(INITIAL_POSITIONS), max(INITIAL_POSITIONS)))}")

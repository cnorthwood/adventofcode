#!/usr/bin/env python3
from collections import defaultdict


def initial_population(filename):
    population = defaultdict(int)
    with open("input.txt") as input_file:
        for days in (int(days) for days in input_file.read().strip().split(",")):
            population[days] += 1
    return population


def iterate(fish):
    next_gen = defaultdict(int)
    next_gen.update({days - 1: num for days, num in fish.items()})
    next_gen[6] += next_gen[-1]
    next_gen[8] += next_gen[-1]
    del next_gen[-1]
    return next_gen


fish = initial_population("input.txt")
for _ in range(80):
    fish = iterate(fish)
print(f"Part One: {sum(fish.values())}")
for _ in range(80, 256):
    fish = iterate(fish)
print(f"Part Two: {sum(fish.values())}")

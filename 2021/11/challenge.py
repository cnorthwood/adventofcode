#!/usr/bin/env python3
from itertools import count


def adj(x, y):
    yield x - 1, y - 1
    yield x - 1, y
    yield x - 1, y + 1
    yield x, y - 1
    yield x, y + 1
    yield x + 1, y - 1
    yield x + 1, y
    yield x + 1, y + 1


def step(octopi):
    flashed = set()
    next_gen = {pos: energy + 1 for pos, energy in octopi.items()}
    while any(energy > 9 for energy in list(next_gen.values())):
        for pos, energy in list(next_gen.items()):
            if energy > 9 and pos not in flashed:
                flashed.add(pos)
                next_gen[pos] = 0
                for neighbour in adj(*pos):
                    if neighbour not in next_gen:
                        continue
                    next_gen[neighbour] += 1
    for flasher in flashed:
        next_gen[flasher] = 0
    return next_gen, len(flashed)


with open("input.txt") as input_file:
    INITIAL = {(x, y): int(c) for (y, line) in enumerate(input_file) for (x, c) in enumerate(line.strip())}


octopi = INITIAL
total = 0
for i in count():
    octopi, flashed = step(octopi)
    total += flashed
    if i == 99:
        print(f"Part One: {total}")
    if flashed == len(octopi):
        print(f"Part Two: {i + 1}")
        break

#!/usr/bin/env python3
import string
from itertools import chain


def compartmentalise(bags):
    for bag in bags:
        yield bag[:len(bag)//2], bag[len(bag)//2:]


def priority(item):
    val = ord(item)
    return val - 96 if val > 96 else val - 38


def chunk(bags):
    for i in range(0, len(bags), 3):
        yield bags[i:i+3]


def find_unique(group):
    return set.intersection(*(set(bag) for bag in group))


with open("input.txt") as input_file:
    INPUT = [line.strip() for line in input_file.readlines()]

print(f"Part One: {sum(priority(item) for item in chain.from_iterable(find_unique(pair) for pair in compartmentalise(INPUT)))}")
print(f"Part Two: {sum(priority(item) for item in chain.from_iterable(find_unique(group) for group in chunk(INPUT)))}")

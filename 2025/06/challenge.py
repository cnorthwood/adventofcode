#!/usr/bin/env python3

from functools import reduce
from operator import mul, add


def load_input(filename):
    with open(filename) as input_file:
        lines = [line.strip().split() for line in input_file.readlines()]
    for i, op in enumerate(lines[-1]):
        yield op, [int(line[i]) for line in lines[:-1]]


OPS = {
    "*": mul,
    "+": add,
}


def part_one(line):
    op, args = line
    return reduce(OPS[op], args)


INPUT = list(load_input("input.txt"))
print(f"Part One: {sum(part_one(line) for line in INPUT)}")

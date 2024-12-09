#!/usr/bin/env -S pypy3 -S

from functools import reduce
from itertools import product
from operator import add, mul


def load_input(input_filename):
    with open(input_filename) as input_file:
        calibrations = []
        for line in input_file:
            expected, operands = line.split(":")
            operands = operands.split()
            calibrations.append((int(expected), list(map(int, operands))))
        return calibrations


def possibly_valid(expected, operands, valid_ops):
    for operators in product(valid_ops, repeat=len(operands) - 1):
        if reduce(lambda a, arg: arg[0](a, arg[1]), zip(operators, operands[1:]), operands[0]) == expected:
            return True
    return False


def concat(a, b):
    return int(str(a) + str(b))


CALIBRATIONS = load_input("input.txt")
print(f"Part One: {sum(expected for expected, operands in CALIBRATIONS if possibly_valid(expected, operands, valid_ops=[add, mul]))}")
print(f"Part Two: {sum(expected for expected, operands in CALIBRATIONS if possibly_valid(expected, operands, valid_ops=[add, mul, concat]))}")

#!/usr/bin/env python3

from functools import reduce
from operator import mul, add


def load_input_part_one(filename):
    with open(filename) as input_file:
        lines = [line.strip().split() for line in input_file.readlines()]
    for i, op in enumerate(lines[-1]):
        yield op, [int(line[i]) for line in lines[:-1]]


OPS = {
    "*": mul,
    "+": add,
}


def apply_ops(line):
    op, args = line
    return reduce(OPS[op], args)


print(f"Part One: {sum(map(apply_ops, load_input_part_one("input.txt")))}")


def load_input_part_two(filename):
    with open(filename) as input_file:
        lines = input_file.read().splitlines()
    column_widths = discover_column_widths(lines[-1])
    return split_into_columns(lines, column_widths)


def discover_column_widths(line):
    column_widths = []
    this_column_width = 1
    for c in line:
        if c in {"*", "+"}:
            column_widths.append(this_column_width - 1)
            this_column_width = 0
        this_column_width += 1
    column_widths.append(this_column_width)
    return column_widths[1:]


def split_into_columns(lines, column_widths):
    i = 0
    for column_width in column_widths:
        op = lines[-1][i:i+column_width].strip()
        args = []
        for column in range(column_width - 1, -1, -1):
            args.append(int("".join(line[i+column] for line in lines[:-1])))
        i += column_width + 1
        yield op, args


print(f"Part Two: {sum(map(apply_ops, load_input_part_two("input.txt")))}")

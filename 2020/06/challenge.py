#!/usr/bin/env python3
from functools import reduce


def parse_data(lines):
    groups = []
    group = []
    for line in lines:
        if line.strip() == "":
            if group:
                groups.append(group)
                group = []
            continue
        group.append(set(line.strip()))

    if len(group):
        groups.append(group)
    return groups


def any_answers(group):
    return reduce(lambda a, i: a.union(i), group)


def all_answers(group):
    return reduce(lambda a, i: a.intersection(i), group)


with open("input.txt") as input_file:
    INPUT = parse_data(input_file.readlines())

print(f"Part One: {sum(len(any_answers(group)) for group in INPUT)}")
print(f"Part Two: {sum(len(all_answers(group)) for group in INPUT)}")

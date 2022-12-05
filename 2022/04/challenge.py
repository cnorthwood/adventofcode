#!/usr/bin/env python3

import re

ASSIGNMENT_RE = re.compile(r'(?P<l1>\d+)-(?P<l2>\d+),(?P<r1>\d+)-(?P<r2>\d+)')


def load_input(filename):
    with open(filename) as input_file:
        for line in input_file:
            match = ASSIGNMENT_RE.match(line.strip())
            yield frozenset(range(int(match.group("l1")), int(match.group("l2")) + 1)), frozenset(range(int(match.group("r1")), int(match.group("r2")) + 1))


def pair_fully_contains(pair):
    return pair[0].issubset(pair[1]) or pair[1].issubset(pair[0])


def pair_overlaps(pair):
    return len(pair[0] & pair[1]) > 0


INPUT = list(load_input("input.txt"))
print(f"Part One: {sum(1 for pair in INPUT if pair_fully_contains(pair))}")
print(f"Part One: {sum(1 for pair in INPUT if pair_overlaps(pair))}")

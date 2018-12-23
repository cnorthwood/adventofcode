#!/usr/bin/env pypy3

from collections import namedtuple
import re

INPUT_RE = re.compile(r'pos=<(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)>, r=(?P<r>\d+)')
Nanobot = namedtuple('Nanobot', 'x y z r')


def load_input(filename):
    with open(filename) as input_file:
        lines = input_file.read().strip().splitlines()
    for line in lines:
        match = INPUT_RE.match(line)
        yield Nanobot(
            x=int(match.group('x')),
            y=int(match.group('y')),
            z=int(match.group('z')),
            r=int(match.group('r')),
        )


TEST = list(load_input('test.txt'))
INPUT = list(load_input('input.txt'))


def get_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def find_largest_nanobot(nanobots):
    return max(nanobots, key=lambda nanobot: nanobot.r)


def get_num_in_range(nanobot, nanobots):
    return sum(1 for n in nanobots if get_distance(nanobot, n) <= nanobot.r)


assert(get_num_in_range(find_largest_nanobot(TEST), TEST) == 7)
print("Part One: {}".format(get_num_in_range(find_largest_nanobot(INPUT), INPUT)))

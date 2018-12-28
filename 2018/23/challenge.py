#!/usr/bin/env pypy3

from collections import namedtuple
import re
from z3 import If, Int, Optimize

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
TEST2 = list(load_input('test2.txt'))
INPUT = list(load_input('input.txt'))


def get_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def find_largest_nanobot(nanobots):
    return max(nanobots, key=lambda nanobot: nanobot.r)


def get_num_in_range(nanobot, nanobots):
    return sum(1 for n in nanobots if get_distance(nanobot, n) <= nanobot.r)


def in_range_of(point, nanobots):
    return sum(1 for n in nanobots if get_distance(point, n) <= n.r)


assert(get_num_in_range(find_largest_nanobot(TEST), TEST) == 7)
print("Part One: {}".format(get_num_in_range(find_largest_nanobot(INPUT), INPUT)))


def zabs(x):
    return If(x >= 0, x, -x)


def find_optimal_space(nanobots):
    (x, y, z) = (Int('x'), Int('y'), Int('z'))
    in_ranges = [
        Int('in_range_{}'.format(i)) for i in range(len(nanobots))
    ]
    range_count = Int('sum')
    optimiser = Optimize()
    for i, nanobot in enumerate(nanobots):
        optimiser.add(in_ranges[i] == If(zabs(x - nanobot.x) + zabs(y - nanobot.y) + zabs(z - nanobot.z) <= nanobot.r, 1, 0))
    optimiser.add(range_count == sum(in_ranges))
    dist_from_zero = Int('dist')
    optimiser.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
    optimiser.maximize(range_count)
    result = optimiser.minimize(dist_from_zero)
    optimiser.check()
    return optimiser.lower(result)


assert(find_optimal_space(TEST2) == 36)
print("Part Two: {}".format(find_optimal_space(INPUT)))

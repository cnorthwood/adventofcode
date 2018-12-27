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


def compress_nanobots(nanobots, factor, min_x, min_y, min_z, max_x, max_y, max_z):
    nanobots = [Nanobot(n.x // factor, n.y // factor, n.z // factor, n.r // factor) for n in nanobots]
    density = {
        (x, y, z): in_range_of(Nanobot(x, y, z, 0), nanobots)
            for x in range(min_x // factor, max_x // factor + 1)
            for y in range(min_y // factor, max_y // factor + 1)
            for z in range(min_z // factor, max_z // factor + 1)
    }
    densest_area = max(density.values())
    return min(
        [(x * factor, y * factor, z * factor, (x + 1) * factor, (y + 1) * factor, (z + 1) * factor) for (x, y, z) in density if density[(x, y, z)] == densest_area],
        key=lambda a: get_distance(Nanobot(0, 0, 0, 0), Nanobot(a[0], a[1], a[2], 0))
    )


def find_optimal_space(nanobots):
    factor = 2**27
    area = (min(n.x for n in nanobots), min(n.y for n in nanobots), min(n.z for n in nanobots), max(n.x for n in nanobots), max(n.y for n in nanobots), max(n.z for n in nanobots))
    while factor > 1:
        factor //= 2
        area = compress_nanobots(nanobots, factor, *area)
    return get_distance(Nanobot(0, 0, 0, 0), Nanobot(area[0], area[1], area[2], 0))


assert(find_optimal_space(TEST2) == 36)
print("Part Two: {}".format(find_optimal_space(INPUT)))

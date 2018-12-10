#!/usr/bin/env pypy3
import operator
import sys
from collections import namedtuple
import re
from itertools import product, count

Particle = namedtuple('Particle', 'position velocity')
INPUT_RE = re.compile(r'position=<(?P<position_x>\s*-?\d+),(?P<position_y>\s*-?\d+)> velocity=<(?P<velocity_x>\s*-?\d+),(?P<velocity_y>\s*-?\d+)>')


def load_particles(filename):
    with open(filename) as input_file:
        return [
            Particle(
                (int(match.group('position_x')), int(match.group('position_y'))),
                (int(match.group('velocity_x')), int(match.group('velocity_y'))),
            ) for match in (INPUT_RE.match(l) for l in input_file.read().strip().splitlines())
        ]


def step(particles):
    return [Particle(tuple(map(operator.add, p.position, p.velocity)), p.velocity) for p in particles]


def print_grid(particles, border=3):
    cells = {p.position for p in particles}
    min_x = min(p[0] for p in cells) - border
    max_x = max(p[0] for p in cells) + border
    min_y = min(p[1] for p in cells) - border
    max_y = max(p[1] for p in cells) + border

    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            sys.stdout.write('#' if (x, y) in cells else '.')
        sys.stdout.write('\n')


def has_neighbour(cell, cells):
    x, y = cell
    return (x - 1, y - 1) in cells or (x - 1, y) in cells or (x - 1, y + 1) in cells \
        or (x, y - 1) in cells or (x, y + 1) in cells \
        or (x + 1, y - 1) in cells or (x + 1, y) in cells or (x + 1, y + 1) in cells


def has_words(particles):
    cells = {p.position for p in particles}
    # let's assume that every cell has at least 1 neighbour
    return all(has_neighbour(cell, cells) for cell in cells)


TEST = load_particles('test.txt')
INPUT = load_particles('input.txt')


def find_message(particles):
    for s in count():
        if has_words(particles):
            print_grid(particles)
            print("Time to align: {}".format(s))
            return
        particles = step(particles)


print('----- TEST ------')
find_message(TEST)

print('----- REAL ------')
find_message(INPUT)

#!/usr/bin/env pypy3

from collections import namedtuple
from math import sqrt
import re

INPUT_RE = re.compile(r'p=<(?P<p_x>-?\d+),(?P<p_y>-?\d+),(?P<p_z>-?\d+)>, v=<(?P<v_x>-?\d+),(?P<v_y>-?\d+),(?P<v_z>-?\d+)>, a=<(?P<a_x>-?\d+),(?P<a_y>-?\d+),(?P<a_z>-?\d+)>')

TEST = """
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
""".strip()

Coordinate = namedtuple('Coordinate', ['x', 'y', 'z'])
Particle = namedtuple('Particle', ['id', 'p', 'v', 'a'])


def build_particles(input):
    for i, line in enumerate(input.splitlines()):
        m = INPUT_RE.match(line)
        yield Particle(
            i,
            Coordinate(
                int(m.group('p_x')),
                int(m.group('p_y')),
                int(m.group('p_z')),
            ),
            Coordinate(
                int(m.group('v_x')),
                int(m.group('v_y')),
                int(m.group('v_z')),
            ),
            Coordinate(
                int(m.group('a_x')),
                int(m.group('a_y')),
                int(m.group('a_z')),
            )
        )


def magnitude(particle):
    return sqrt(particle.a.x ** 2 + particle.a.y ** 2 + particle.a.z ** 2)


def closest(particles):
    return sorted(particles, key=magnitude)[0]


TEST_PARTICLES = list(build_particles(TEST))
with open('input.txt') as INPUT:
    PARTICLES = list(build_particles(INPUT.read()))

assert closest(TEST_PARTICLES).id == 0
print("Part One:", closest(PARTICLES).id)

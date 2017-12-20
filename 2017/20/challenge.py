#!/usr/bin/env pypy3

from collections import namedtuple, defaultdict
from math import sqrt
import re

INPUT_RE = re.compile(r'p=<(?P<p_x>-?\d+),(?P<p_y>-?\d+),(?P<p_z>-?\d+)>, v=<(?P<v_x>-?\d+),(?P<v_y>-?\d+),(?P<v_z>-?\d+)>, a=<(?P<a_x>-?\d+),(?P<a_y>-?\d+),(?P<a_z>-?\d+)>')

TEST = """
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
""".strip()

TEST2 = """
p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>    
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>
""".strip()

Particle = namedtuple('Particle', ['id', 'p', 'v', 'a'])


def build_particles(input):
    for i, line in enumerate(input.splitlines()):
        m = INPUT_RE.match(line)
        yield Particle(
            i,
            [
                int(m.group('p_x')),
                int(m.group('p_y')),
                int(m.group('p_z')),
            ],
            [
                int(m.group('v_x')),
                int(m.group('v_y')),
                int(m.group('v_z')),
            ],
            [
                int(m.group('a_x')),
                int(m.group('a_y')),
                int(m.group('a_z')),
            ]
        )


def magnitude(particle):
    return sqrt(particle.a[0] ** 2 + particle.a[1] ** 2 + particle.a[2] ** 2)


def closest(particles):
    return sorted(particles, key=magnitude)[0]


def tick(particles):
    for particle in particles:
        particle.v[0] += particle.a[0]
        particle.v[1] += particle.a[1]
        particle.v[2] += particle.a[2]
        particle.p[0] += particle.v[0]
        particle.p[1] += particle.v[1]
        particle.p[2] += particle.v[2]


def remove_collided(particles):
    positions = defaultdict(list)
    tidied_particles = []
    for particle in particles:
        positions[(particle.p[0], particle.p[1], particle.p[2])].append(particle)
    for particles_here in positions.values():
        if len(particles_here) == 1:
            tidied_particles += particles_here
    return tidied_particles


TEST_PARTICLES = list(build_particles(TEST))
with open('input.txt') as INPUT:
    PARTICLES = list(build_particles(INPUT.read()))

assert closest(TEST_PARTICLES).id == 0
print("Part One:", closest(PARTICLES).id)

TEST2_PARTICLES = list(build_particles(TEST2))
test2_particles = remove_collided(TEST2_PARTICLES)
for _ in range(4):
    tick(test2_particles)
    test2_particles = remove_collided(test2_particles)

assert len(test2_particles) == 1


particles = remove_collided(PARTICLES)
for _ in range(10000):
    tick(particles)
    particles = remove_collided(particles)
print("Part Two:", len(particles))

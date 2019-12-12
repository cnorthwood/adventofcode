#!/usr/bin/env pypy3

from collections import namedtuple
from itertools import count, combinations
from math import gcd
import re

INPUT_RE = re.compile(r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>')
Moon = namedtuple("Moon", "pos vel")


def apply_gravity(moon_a, moon_b, dimension):
    if moon_a.pos[dimension] < moon_b.pos[dimension]:
        moon_a.vel[dimension] += 1
        moon_b.vel[dimension] -= 1
    elif moon_a.pos[dimension] > moon_b.pos[dimension]:
        moon_a.vel[dimension] -= 1
        moon_b.vel[dimension] += 1


def apply_velocity(moon):
    moon.pos["x"] += moon.vel["x"]
    moon.pos["y"] += moon.vel["y"]
    moon.pos["z"] += moon.vel["z"]


def step(moons):
    for moon_a, moon_b in combinations(moons, 2):
        for dimension in "xyz":
            apply_gravity(moon_a, moon_b, dimension)
    for moon in moons:
        apply_velocity(moon)


def total_energy(moons):
    return sum(sum(abs(v) for v in moon.pos.values()) * sum(abs(v) for v in moon.vel.values()) for moon in moons)


def parse_lines(lines):
    for line in lines:
        if line == "":
            continue
        match = INPUT_RE.match(line)
        if match is None:
            raise IOError()
        yield Moon(
            pos={"x": int(match.group("x")), "y": int(match.group("y")), "z": int(match.group("z"))},
            vel={"x": 0, "y": 0, "z": 0}
        )


def init_moons():
    with open("input.txt") as input_file:
        return list(parse_lines(input_file.readlines()))


def find_total_energy(steps=1000):
    moons = init_moons()
    for _ in range(steps):
        step(moons)
    return total_energy(moons)


def find_cycle(dimension):
    moons = init_moons()
    initial_state = [(pos[dimension], vel[dimension]) for pos, vel in moons]
    for i in count():
        step(moons)
        if [(pos[dimension], vel[dimension]) for pos, vel in moons] == initial_state:
            return i + 1


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


print(f"Part One: {find_total_energy()}")
print(f"Part Two: {lcm(lcm(find_cycle('x'), find_cycle('y')), find_cycle('z'))}")
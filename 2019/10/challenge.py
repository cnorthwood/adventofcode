#!/usr/bin/env python3

from collections import defaultdict
from math import atan2, hypot, pi


def distance_between(a, b):
    return hypot(b[0] - a[0], b[1] - a[1])


def angle_between(a, b):
    angle = -atan2(b[1] - a[1], b[0] - a[0])
    return angle if angle >= -pi/2 else angle + 2 * pi


def detectable_from(candidate, asteroids):
    detectable = set()
    for asteroid in asteroids:
        if candidate == asteroid:
            continue
        detectable.add(angle_between(candidate, asteroid))
    return len(detectable)


def destruction_order(station, asteroids):
    to_destroy = defaultdict(list)
    for asteroid in asteroids:
        if asteroid == station:
            continue
        to_destroy[angle_between(station, asteroid)].append(asteroid)
    for angle in to_destroy.keys():
        to_destroy[angle].sort(key=lambda asteroid: distance_between(station, asteroid), reverse=True)
    while to_destroy:
        for angle in sorted(to_destroy.keys()):
            yield to_destroy[angle].pop()
            if not to_destroy[angle]:
                del to_destroy[angle]


def challenge(filename):
    asteroids = set()
    with open(filename) as input_file:
        for y, line in enumerate(input_file.readlines()):
            for x, c in enumerate(line):
                if c == "#":
                    asteroids.add((x, -y))

    best_asteroid = max(asteroids, key=lambda asteroid: detectable_from(asteroid, asteroids))
    for i, asteroid in enumerate(destruction_order(best_asteroid, asteroids)):
        if i == 199:
            return detectable_from(best_asteroid, asteroids), asteroid[0] * 100 - asteroid[1]


part_one, part_two = challenge("input.txt")
print(f"Part One: {part_one}")
print(f"Part Two: {part_two}")
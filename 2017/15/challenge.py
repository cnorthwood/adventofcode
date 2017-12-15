#!/usr/bin/env pypy3

FACTOR_A = 16807
FACTOR_B = 48271
START_A = 883
START_B = 879


def generate(start, factor):
    return start * factor % 2147483647


def build_generator(n, factor, limit=40000000):
    for _ in range(limit):
        n = generate(n, factor)
        yield n


def lowest16_matches(pair):
    a, b = pair
    return a & 65535 == b & 65535


assert generate(65, factor=FACTOR_A) == 1092455
assert generate(8921, factor=FACTOR_B) == 430625591
assert lowest16_matches((245556042, 1431495498))

print("Part One:", sum(1 for _ in filter(lowest16_matches, zip(
    build_generator(START_A, FACTOR_A),
    build_generator(START_B, FACTOR_B),
))))

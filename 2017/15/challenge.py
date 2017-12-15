#!/usr/bin/env pypy3

FACTOR_A = 16807
FACTOR_B = 48271
START_A = 883
START_B = 879


def generate(start, factor):
    return start * factor % 2147483647


def build_generator(start, factor, mult, limit=40000000):
    n = generate(start, factor)
    for _ in range(limit):
        while n % mult > 0:
            n = generate(n, factor)
        yield n
        n = generate(n, factor)


def lowest16_matches(pair):
    a, b = pair
    return a & 65535 == b & 65535


assert generate(65, factor=FACTOR_A) == 1092455
assert generate(8921, factor=FACTOR_B) == 430625591

gen_a = build_generator(65, FACTOR_A, 1)
gen_b = build_generator(8921, FACTOR_B, 1)

assert next(gen_a) == 1092455
assert next(gen_a) == 1181022009
assert next(gen_b) == 430625591
assert next(gen_b) == 1233683848

gen_a = build_generator(65, FACTOR_A, 4)
gen_b = build_generator(8921, FACTOR_B, 8)

assert next(gen_a) == 1352636452
assert next(gen_a) == 1992081072
assert next(gen_b) == 1233683848
assert next(gen_b) == 862516352

assert lowest16_matches((245556042, 1431495498))

print("Part One:", sum(1 for _ in filter(lowest16_matches, zip(
    build_generator(START_A, FACTOR_A, 1, 40000000),
    build_generator(START_B, FACTOR_B, 1, 40000000),
))))

print("Part Two:", sum(1 for _ in filter(lowest16_matches, zip(
    build_generator(START_A, FACTOR_A, 4, 5000000),
    build_generator(START_B, FACTOR_B, 8, 5000000),
))))

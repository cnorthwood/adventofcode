#!/usr/bin/env python3

from functools import cache


def load_input(filename):
    with open(filename) as input_file:
        return [tuple(int(x) for x in part.split("-")) for part in input_file.read().strip().split(",")]


def is_repeating(s, n):
    return s == s[:len(s) // n] * n



def invalid_ids_part_one(r):
    for i in range(r[0], r[1] + 1):
        s = str(i)
        if len(s) % 2 != 0:
            continue
        if is_repeating(s, 2):
            yield i


@cache
def factors(n):
    r = []
    for i in range(2, n + 1):
        if n % i == 0:
            r.append(i)
    return r


def invalid_ids_part_two(r):
    for i in range(r[0], r[1] + 1):
        s = str(i)
        for factor in factors(len(s)):
            if is_repeating(s, factor):
                yield i
                break


# print(sum(sum(invalid_ids_part_two(r)) for r in load_input('test.txt')))

INPUT = load_input("input.txt")

print(f"Part One: {sum(sum(invalid_ids_part_one(r)) for r in INPUT)}")
print(f"Part Two: {sum(sum(invalid_ids_part_two(r)) for r in INPUT)}")

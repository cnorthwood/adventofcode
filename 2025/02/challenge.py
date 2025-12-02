#!/usr/bin/env python3


with open("input.txt") as input_file:
    INPUT = [tuple(int(x) for x in part.split("-")) for part in input_file.read().strip().split(",")]


def invalid_ids(r):
    for i in range(r[0], r[1] + 1):
        s = str(i)
        if len(s) % 2 != 0:
            continue
        if s[:len(s)//2] == s[len(s)//2:]:
            yield i


print(f"Part One: {sum(sum(invalid_ids(r)) for r in INPUT)}")

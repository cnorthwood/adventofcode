#!/usr/bin/env python3 -S

import re

with open("input.txt") as input_file:
    INPUT = input_file.read().strip()

MUL_RE = re.compile(r'mul\((?P<a>\d+),(?P<b>\d+)\)')
PART2_RE = re.compile(r'((?P<on>do)\(\)|(?P<off>don\'t)\(\)|(?P<mul>mul)\((?P<a>\d+),(?P<b>\d+)\))')


def process_ops(ops):
    muls_enabled = True
    a = 0
    for match in PART2_RE.finditer(INPUT):
        if match.group("on"):
            muls_enabled = True
        elif match.group("off"):
            muls_enabled = False
        elif match.group("mul") and muls_enabled:
            a += int(match.group('a')) * int(match.group('b'))
    return a


print(f"Part One: {sum(int(mul_expr_match.group('a')) * int(mul_expr_match.group('b')) for mul_expr_match in MUL_RE.finditer(INPUT))}")
print(f"Part Two: {process_ops(INPUT)}")

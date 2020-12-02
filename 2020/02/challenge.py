#!/usr/bin/env python3

import re

LINE_RE = re.compile(r'(?P<lower>\d+)-(?P<upper>\d+) (?P<char>\w): (?P<password>\w+)')

INPUT = []

with open("input.txt") as puzzle_input:
    for line in puzzle_input:
        match = LINE_RE.match(line)
        INPUT.append({
            "lower": int(match.group("lower")),
            "upper": int(match.group("upper")),
            "char": match.group("char"),
            "password": match.group("password"),
        })


def is_valid_part1(line):
    num_chars = sum(1 for char in line["password"] if char == line["char"])
    return line["lower"] <= num_chars <= line["upper"]


def is_valid_part2(line):
    in_pos1 = line["password"][line["lower"] - 1] == line["char"]
    in_pos2 = line["password"][line["upper"] - 1] == line["char"]
    return (in_pos1 and not in_pos2) or (in_pos2 and not in_pos1)


assert is_valid_part1({"lower": 1, "upper": 3, "char": "a", "password": "abcde"})
assert not is_valid_part1({"lower": 1, "upper": 3, "char": "b", "password": "cdefg"})
assert is_valid_part1({"lower": 2, "upper": 9, "char": "c", "password": "ccccccccc"})
assert is_valid_part2({"lower": 1, "upper": 3, "char": "a", "password": "abcde"})
assert not is_valid_part2({"lower": 1, "upper": 3, "char": "b", "password": "cdefg"})
assert not is_valid_part2({"lower": 2, "upper": 9, "char": "c", "password": "ccccccccc"})


print(f"Part One: {sum(1 for line in INPUT if is_valid_part1(line))}")
print(f"Part Two: {sum(1 for line in INPUT if is_valid_part2(line))}")

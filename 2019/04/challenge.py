#!/usr/bin/env pypy3

from collections import Counter
import re

DUPLICATED_NUMBER_RE = re.compile(r'(\d)\1')


def is_valid_password(password):
    return "".join(sorted(password)) == password and DUPLICATED_NUMBER_RE.search(password) is not None


def is_part2_valid(password):
    return 2 in Counter(password).values()


def find_valid_passwords(start, end):
    for potential in range(start, end):
        if is_valid_password(str(potential)):
            yield potential


with open("input.txt") as input_file:
    INPUT_START, INPUT_END = [int(part) for part in input_file.read().split("-")]


PART_ONE_PASSWORDS = list(str(potential) for potential in range(INPUT_START, INPUT_END) if is_valid_password(str(potential)))
print(f"Part One: {len(PART_ONE_PASSWORDS)}")
print(f"Part Two: {len(list(password for password in PART_ONE_PASSWORDS if is_part2_valid(password)))}")

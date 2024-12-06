#!/usr/bin/env -S python3 -S

from collections import Counter

with open("input.txt") as input_file:
    PAIRS = [tuple(map(int, line.split())) for line in input_file]

SORTED_PAIRS = zip(sorted(pair[0] for pair in PAIRS), sorted(pair[1] for pair in PAIRS))
MULTIPLIERS = Counter(pair[1] for pair in PAIRS)

print(f"Part One: {sum(abs(pair[0] - pair[1]) for pair in SORTED_PAIRS)}")
print(f"Part Two: {sum(value * MULTIPLIERS[value] for (value, _) in PAIRS)}")

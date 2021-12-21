#!/usr/bin/env python3

from collections import defaultdict, Counter
from math import ceil


def load_input(filename):
    with open(filename) as input_file:
        polymer = next(input_file).strip()
        rules = {}
        for line in input_file:
            if not line.strip(): continue
            pair, insertion = line.strip().split(" -> ")
            rules[tuple(pair)] = insertion
    pair_counter = defaultdict(int)
    for a, b in zip(polymer, polymer[1:]):
        pair_counter[a, b] += 1
    return pair_counter, b, rules


def apply(pair_counter, rules):
    next_counter = defaultdict(int)
    for (a, b), n in pair_counter.items():
        if (a, b) in rules:
            next_counter[a, rules[a, b]] += n
            next_counter[rules[a, b], b] += n
        else:
            next_counter[a, b] = n
    return next_counter


def polymer_value(pair_counter, last_c):
    c = Counter()
    # Take into account last character as it only appears on one side of a production
    c[last_c] += 1
    for (a, b), n in pair_counter.items():
        c[a] += n
    return max(c.values()) - min(c.values())


pair_counter, last_c, RULES = load_input("input.txt")
for i in range(40):
    pair_counter = apply(pair_counter, RULES)
    if i == 9:
        print(f"Part One: {polymer_value(pair_counter, last_c)}")
print(f"Part Two: {polymer_value(pair_counter, last_c)}")

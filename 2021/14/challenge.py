#!/usr/bin/env python3

from collections import defaultdict, Counter


def load_input(filename):
    with open(filename) as input_file:
        initial = next(input_file).strip()
        rules = defaultdict(str)
        for line in input_file:
            if not line.strip(): continue
            pair, insertion = line.strip().split(" -> ")
            rules[tuple(pair)] = insertion
    return initial, rules


def apply(polymer, rules):
    complete = ""
    for a, b in zip(polymer, polymer[1:]):
        complete += f"{a}{rules[a, b]}"
    complete += b
    return complete


def polymer_value(polymer):
    c = Counter(polymer)
    return max(c.values()) - min(c.values())


polymer, RULES = load_input("input.txt")
for i in range(10):
    polymer = apply(polymer, RULES)
    if i == 9:
        print(f"Part One: {polymer_value(polymer)}")

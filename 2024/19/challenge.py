#!/usr/bin/env -S pypy3 -S

from functools import cache

def load_input(input_filename):
    with open(input_filename) as input_file:
        towels = next(input_file).strip().split(", ")
        next(input_file)
        combos = [line.strip() for line in input_file]
        return towels, combos


@cache
def valid_combo(combo):
    if combo == "":
        return True
    else:
        return any(valid_combo(combo[len(towel):]) for towel in TOWELS if combo.startswith(towel))


TOWELS, COMBOS = load_input("input.txt")
print(f"Part One: {sum(1 for combo in COMBOS if valid_combo(combo))}")

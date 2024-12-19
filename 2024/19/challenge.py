#!/usr/bin/env -S pypy3 -S

from functools import cache

def load_input(input_filename):
    with open(input_filename) as input_file:
        towels = next(input_file).strip().split(", ")
        next(input_file)
        combos = [line.strip() for line in input_file]
        return towels, combos


@cache
def arrangements_for_combo(combo):
    if combo == "":
        return 1
    else:
        return sum(arrangements_for_combo(combo[len(towel):]) for towel in TOWELS if combo.startswith(towel))


TOWELS, COMBOS = load_input("input.txt")
VALID_ARRANGEMENTS = {combo: arrangements_for_combo(combo) for combo in COMBOS}
print(f"Part One: {sum(1 for n in VALID_ARRANGEMENTS.values() if n > 0)}")
print(f"Part Two: {sum(VALID_ARRANGEMENTS.values())}")

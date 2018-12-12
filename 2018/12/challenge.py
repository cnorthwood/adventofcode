#!/usr/bin/env pypy3

from collections import defaultdict
import sys


def convert_input_to_bool(d):
    return tuple(c == '#' for c in d)


def load_data(filename):
    with open(filename) as input_file:
        lines = input_file.read().strip().splitlines()
    initial = defaultdict(bool)
    initial.update({i: c for i, c in enumerate(convert_input_to_bool(lines[0].split(': ')[1]))})
    rules = [tuple(map(convert_input_to_bool, line.split(' => '))) for line in lines[2:]]
    return initial, rules


def print_state(state):
    for i in range(min(state.keys()), max(state.keys()) + 1):
        sys.stdout.write('#' if state[i] else '.')
    sys.stdout.write('\n')


TEST_INITIAL, TEST_RULES = load_data('test.txt')
INITIAL, RULES = load_data('input.txt')


def iterate(gen, rules):
    next_gen = defaultdict(bool)
    for i in range(min(gen.keys()) - 2, max(gen.keys()) + 3):
        for match, result in rules:
            if (gen[i-2], gen[i-1], gen[i], gen[i+1], gen[i+2]) == match:
                next_gen[i] = result[0]
                break
    return next_gen


def part_one(iterations, state, rules):
    for _ in range(iterations):
        state = iterate(state, rules)
        # print_state(state)
    return sum(pot_id for pot_id, has_plant in state.items() if has_plant)


assert(part_one(20, TEST_INITIAL, TEST_RULES) == 325)
print("Part One: {}".format(part_one(20, INITIAL, RULES)))
print("Part Two: {}".format(part_one(50000000000, INITIAL, RULES)))

#!/usr/bin/env pypy3


def compute_drift(sequence):
    c = 0
    for item in sequence:
        c += int(item)
    return c


TEST = [
    ('+1, -2, +3, +1'.split(', '), 3),
    ('+1, +1, +1'.split(', '), 3),
    ('+1, +1, -2'.split(', '), 0),
    ('-1, -2, -3'.split(', '), -6),
]

with open('input.txt') as input_fd:
    INPUT = input_fd.read().splitlines()

for sequence, expected in TEST:
    assert(compute_drift(sequence) == expected)

print("Part One: {}".format(compute_drift(INPUT)))

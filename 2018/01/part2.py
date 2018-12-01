#!/usr/bin/env pypy3


def find_repeated(sequence):
    c = 0
    seen = {0}
    while True:
        for item in sequence:
            c += int(item)
            if c in seen:
                return c
            seen.add(c)


TEST = [
    ('+1, -1'.split(', '), 0),
    ('+3, +3, +4, -2, -4'.split(', '), 10),
    ('-6, +3, +8, +5, -6'.split(', '), 5),
    ('+7, +7, -2, -7, -4'.split(', '), 14),
]

with open('input.txt') as input_fd:
    INPUT = input_fd.read().splitlines()

for sequence, expected in TEST:
    assert(find_repeated(sequence) == expected)

print("Part Two: {}".format(find_repeated(INPUT)))

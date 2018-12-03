#!/usr/bin/env pypy3
from itertools import count


def compute_drift(sequence):
    c = 0
    seen = {c}
    for i in count():
        for item in sequence:
            c += int(item)
            if c in seen:
                print("Part Two: {}".format(c))
                return
            seen.add(c)
        if i == 0:
            print("Part One: {}".format(c))


with open('input.txt') as input_fd:
    INPUT = input_fd.read().splitlines()

compute_drift(INPUT)

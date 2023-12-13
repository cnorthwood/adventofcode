#!/usr/bin/env python3


def load_input(filename):
    with open(filename) as input_file:
        for line in input_file:
            yield [int(n) for n in line.split()]


def predict_next(ns):
    if all(n == 0 for n in ns):
        return ns[0]

    return ns[-1] + predict_next([b - a for a, b in zip(ns, ns[1:])])


INPUT = list(load_input("input.txt"))
print(f"Part One: {sum(predict_next(ns) for ns in INPUT)}")
print(f"Part Two: {sum(predict_next(list(reversed(ns))) for ns in INPUT)}")

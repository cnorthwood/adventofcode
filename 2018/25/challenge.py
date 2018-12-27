#!/usr/bin/env pypy3


def load_input(filename):
    with open(filename) as input_file:
        return [{tuple(map(int, line.split(',')))} for line in input_file.read().strip().splitlines()]


def distance(a, b):
    return sum(abs(c0 - c1) for (c0, c1) in zip(a, b))


def has_overlap(c1, c2):
    for a in c1:
        for b in c2:
            if distance(a, b) <= 3:
                return True
    return False


def merge_sets(constellations):
    num_constellations = 0
    while len(constellations) != num_constellations:
        num_constellations = len(constellations)
        for constellation in constellations:
            for other_constellation in constellations:
                if other_constellation == constellation:
                    continue
                if has_overlap(constellation, other_constellation):
                    constellations.remove(other_constellation)
                    constellation.update(other_constellation)
    return len(constellations)


assert(merge_sets(load_input('test.txt')) == 2)
print("Part One: {}".format(merge_sets(load_input('input.txt'))))

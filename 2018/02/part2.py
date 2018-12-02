#!/usr/bin/env pypy3

from itertools import product


TEST = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""".splitlines()


def hamming_distance(pair):
    a, b = pair
    distance = 0
    for i, c in enumerate(a):
        if c != b[i]:
            distance += 1
    return distance


def similar_box_ids(boxes):
    return sorted(filter(lambda pair: pair[0] != pair[1], product(boxes, repeat=2)), key=hamming_distance)[0]


assert(similar_box_ids(TEST) == ('fghij', 'fguij'))


def matching_letters(pair):
    a, b = pair
    s = ''
    for i, c in enumerate(a):
        if c == b[i]:
            s += c
    return s


assert(matching_letters(('fghij', 'fguij')) == 'fgij')

with open('input.txt') as input_file:
    print("Part Two: {}".format(matching_letters(similar_box_ids(input_file.read().splitlines()))))

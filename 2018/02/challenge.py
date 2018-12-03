#!/usr/bin/env pypy3

from collections import Counter
from itertools import product


TEST1 = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""".splitlines()

TEST2 = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""".splitlines()


def count_dupes(box):
    counter = Counter(box)
    return 2 in counter.values(), 3 in counter.values()


# assert(count_dupes(TEST1[0]) == (False, False))
# assert(count_dupes(TEST1[1]) == (True, True))
# assert(count_dupes(TEST1[2]) == (True, False))
# assert(count_dupes(TEST1[3]) == (False, True))
# assert(count_dupes(TEST1[4]) == (True, False))
# assert(count_dupes(TEST1[5]) == (True, False))
# assert(count_dupes(TEST1[6]) == (False, True))


def generate_checksum(boxes):
    twos = 0
    threes = 0
    for box in boxes:
        has_two, has_three = count_dupes(box)
        if has_two:
            twos += 1
        if has_three:
            threes += 1
    return twos * threes


# assert(generate_checksum(TEST1) == 12)


def hamming_distance(pair):
    a, b = pair
    distance = 0
    for i, c in enumerate(a):
        if c != b[i]:
            distance += 1
    return distance


def similar_box_ids(boxes):
    return sorted(filter(lambda pair: pair[0] != pair[1], product(boxes, repeat=2)), key=hamming_distance)[0]


# assert(similar_box_ids(TEST2) == ('fghij', 'fguij'))


def matching_letters(pair):
    a, b = pair
    s = ''
    for i, c in enumerate(a):
        if c == b[i]:
            s += c
    return s


# assert(matching_letters(('fghij', 'fguij')) == 'fgij')


with open('input.txt') as input_file:
    INPUT = input_file.read().splitlines()

print("Part One: {}".format(generate_checksum(INPUT)))
print("Part Two: {}".format(matching_letters(similar_box_ids(INPUT))))

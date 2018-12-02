#!/usr/bin/env pypy3

from collections import Counter


TEST = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""".splitlines()


def count_dupes(box):
    counter = Counter(box)
    return 2 in counter.values(), 3 in counter.values()


assert(count_dupes(TEST[0]) == (False, False))
assert(count_dupes(TEST[1]) == (True, True))
assert(count_dupes(TEST[2]) == (True, False))
assert(count_dupes(TEST[3]) == (False, True))
assert(count_dupes(TEST[4]) == (True, False))
assert(count_dupes(TEST[5]) == (True, False))
assert(count_dupes(TEST[6]) == (False, True))


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

assert(generate_checksum(TEST) == 12)

with open('input.txt') as input_file:
    print("Part One: {}".format(generate_checksum(input_file.readlines())))

#!/usr/bin/env python3

from functools import reduce


def rotate(start, length, data):
    slots = [None] * len(data)
    for i in range(length):
        slots[(start + i) % len(data)] = data[(start + length - i - 1) % len(data)]
    for i, slot in enumerate(slots):
        if slot is None:
            slots[i] = data[i]
    return slots


assert rotate(0, 3, [0, 1, 2, 3, 4]) == [2, 1, 0, 3, 4]
assert rotate(3, 4, [2, 1, 0, 3, 4]) == [4, 3, 0, 1, 2]


INPUT = "106,118,236,1,130,0,235,254,59,205,2,87,129,25,255,118"


def hash_round(input, data, current_location, start_skip):
    for skip, item in enumerate(input):
        data = rotate(current_location, item, data)
        current_location += start_skip + skip + item
    return data, current_location


def multi_rounds(input, rounds=64):
    input = list(map(ord, input)) + [17, 31, 73, 47, 23]
    data = list(range(256))
    current_location = 0
    for i in range(rounds):
        data, current_location = hash_round(input, data, current_location, i * len(input))
    return data


def dense_hash(sparse_hash):
    hash = ""
    while sparse_hash:
        group, sparse_hash = sparse_hash[:16], sparse_hash[16:]
        hash += '{:02x}'.format(reduce(lambda a, b: a ^ b, group))
    return hash


assert dense_hash(multi_rounds("")) == "a2582a3a0e66e6e86e3812dcb672a272"
assert dense_hash(multi_rounds("AoC 2017")) == "33efeb34ea91902bb2f59c9920caa6cd"
assert dense_hash(multi_rounds("1,2,3")) == "3efbe78a8d82f29979031a4aa0b16a9d"
assert dense_hash(multi_rounds("1,2,4")) == "63960835bcdc130f0b66d7ff4f6a5a8e"

part1 = hash_round(map(int, INPUT.split(',')), list(range(256)), 0, 0)[0]
print("Part One:", part1[0] * part1[1])
print("Part Two:", dense_hash(multi_rounds(INPUT)))

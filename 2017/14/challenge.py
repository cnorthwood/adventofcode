#!/usr/bin/env python3

INPUT = "hwlqcszp"

from functools import reduce
from itertools import chain


def rotate(start, length, data):
    slots = [None] * len(data)
    for i in range(length):
        slots[(start + i) % len(data)] = data[(start + length - i - 1) % len(data)]
    for i, slot in enumerate(slots):
        if slot is None:
            slots[i] = data[i]
    return slots


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


def knot_hash(input):
    sparse_hash = multi_rounds(input)
    hash = ""
    while sparse_hash:
        group, sparse_hash = sparse_hash[:16], sparse_hash[16:]
        hash += '{:02x}'.format(reduce(lambda a, b: a ^ b, group))
    return hash


BITS = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111',
}


def active_in_row(row):
    bits = ''.join(chain(BITS[c] for c in row))
    return len(list(filter(lambda bit: bit == '1', bits)))


def active(input):
    return sum(active_in_row(knot_hash('{}-{}'.format(input, i))) for i in range(128))


assert active('flqrgnkx') == 8108
print("Part One:", active(INPUT))

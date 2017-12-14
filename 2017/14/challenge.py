#!/usr/bin/env pypy3

INPUT = 'hwlqcszp'
TEST_INPUT = 'flqrgnkx'


from functools import reduce
from itertools import chain
from sys import setrecursionlimit

setrecursionlimit(128 * 128)


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


def build_row(row):
    return ''.join(chain(BITS[c] for c in row))


def active(grid):
    return len(list(filter(lambda bit: bit == '1', grid.values())))


def build_grid(input):
    return {(x, y): bit for y in range(128) for x, bit in enumerate(build_row(knot_hash('{}-{}'.format(input, y))))}


def find_connected(start, group, grid):
    group.add(start)
    x, y = start
    neighbours = [
        (x - 1, y),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y),
    ]
    for neighbour in neighbours:
        if neighbour in grid and neighbour not in group and grid[neighbour] == '1':
            find_connected(neighbour, group, grid)


def group_all(grid):
    groups = {}
    group_count = 0
    for x in range(128):
        for y in range(128):
            if grid[(x, y)] == '1' and (x, y) not in groups:
                group_count += 1
                group = set()
                find_connected((x, y), group, grid)
                for member in group:
                    groups[member] = group_count
    return group_count


GRID = build_grid(INPUT)
TEST_GRID = build_grid(TEST_INPUT)

assert active(TEST_GRID) == 8108
print("Part One:", active(GRID))

assert group_all(TEST_GRID) == 1242
print("Part Two:", group_all(GRID))

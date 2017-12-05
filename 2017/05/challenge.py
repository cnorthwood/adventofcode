#!/usr/bin/env python3

TEST = [0, 3, 0, 1, -3]


def step(ptr, mem):
    target = ptr + mem[ptr]
    mem[ptr] += 1
    if target < 0 or target >= len(mem):
        return None
    return target


def num_jumps(mem):
    ptr = 0
    i = 0
    while ptr is not None:
        i += 1
        ptr = step(ptr, mem)
    return i


assert step(0, TEST) == 0
assert TEST == [1, 3, 0, 1, -3]

assert step(0, TEST) == 1
assert TEST == [2, 3, 0, 1, -3]

assert step(1, TEST) == 4
assert TEST == [2, 4, 0, 1, -3]

assert step(4, TEST) == 1
assert TEST == [2, 4, 0, 1, -2]

assert step(1, TEST) is None
assert TEST == [2, 5, 0, 1, -2]

assert num_jumps([0, 3, 0, 1, -3]) == 5

with open('input.txt') as input:
    INPUT = list(map(int, input.readlines()))
    print("Part One:", num_jumps(INPUT))

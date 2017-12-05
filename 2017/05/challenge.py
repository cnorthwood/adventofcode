#!/usr/bin/env python3

TEST = [0, 3, 0, 1, -3]


def step1(ptr, mem):
    target = ptr + mem[ptr]
    mem[ptr] += 1
    if target < 0 or target >= len(mem):
        return None
    return target


def step2(ptr, mem):
    target = ptr + mem[ptr]
    if mem[ptr] >= 3:
        mem[ptr] -= 1
    else:
        mem[ptr] += 1
    if target < 0 or target >= len(mem):
        return None
    return target


def num_jumps(mem, step):
    ptr = 0
    i = 0
    while ptr is not None:
        i += 1
        ptr = step(ptr, mem)
    return i


assert step1(0, TEST) == 0
assert TEST == [1, 3, 0, 1, -3]

assert step1(0, TEST) == 1
assert TEST == [2, 3, 0, 1, -3]

assert step1(1, TEST) == 4
assert TEST == [2, 4, 0, 1, -3]

assert step1(4, TEST) == 1
assert TEST == [2, 4, 0, 1, -2]

assert step1(1, TEST) is None
assert TEST == [2, 5, 0, 1, -2]

assert num_jumps([0, 3, 0, 1, -3], step1) == 5
assert num_jumps([0, 3, 0, 1, -3], step2) == 10

with open('input.txt') as input:
    INPUT = list(map(int, input.readlines()))
    print("Part One:", num_jumps(list(INPUT), step1))
    print("Part Two:", num_jumps(list(INPUT), step2))

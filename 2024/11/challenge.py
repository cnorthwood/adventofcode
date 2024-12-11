#!/usr/bin/env -S pypy3 -S

from functools import cache

def blink(stone):
    if stone == "0":
        return ["1"]
    elif len(stone) % 2 == 0:
        return [stone[:len(stone) // 2], str(int(stone[len(stone) // 2:]))]
    else:
        return [str(int(stone) * 2024)]


@cache
def expanded_stone(n, stone):
    if n == 0:
        return 1
    return sum(expanded_stone(n - 1, substone) for substone in blink(stone))


def expanded_length(n, stones):
    return sum(expanded_stone(n, stone) for stone in stones)


with open("input.txt") as input_file:
    INPUT = input_file.read().split()


print(f"Part One: {expanded_length(25, INPUT)}")
print(f"Part Two: {expanded_length(75, INPUT)}")

#!/usr/bin/env python3

from itertools import combinations

with open("input.txt") as input_file:
    INPUT = [int(line.strip()) for line in input_file]


def is_number_valid(history):
    pairs = history[-26:-1]
    number_to_consider = history[-1]
    for combination in combinations(pairs, 2):
        if sum(combination) == number_to_consider:
            return True
    else:
        return False


def find_contiguous_range(values, target):
    for size in range(2, len(values)):
        for start in range(len(values) - size):
            for end in range(start, len(values)):
                if sum(values[start:end]) == target:
                    return min(values[start:end]) + max(values[start:end])


for i in range(25, len(INPUT)):
    if not is_number_valid(INPUT[:i+1]):
        invalid_number = INPUT[i]
        print(f"Part One: {invalid_number}")
        print(f"Part Two: {find_contiguous_range(INPUT, invalid_number)}")
        break

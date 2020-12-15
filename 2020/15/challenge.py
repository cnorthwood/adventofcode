#!/usr/bin/env pypy3

with open("input.txt") as input_file:
    INPUT = [int(n) for n in input_file.read().split(",")]


def calculate_next_number(last_number, seen_indexes):
    if len(seen_indexes[last_number]) == 1:
        return 0
    else:
        return seen_indexes[last_number][-1] - seen_indexes[last_number][-2]


def find_number(starting_numbers, target):
    seen_indexes = {n: [i] for i, n in enumerate(starting_numbers)}
    last_number = starting_numbers[-1]
    for i in range(len(starting_numbers), target):
        next_number = calculate_next_number(last_number, seen_indexes)
        seen_indexes[next_number] = [seen_indexes[next_number][-1], i] if next_number in seen_indexes else [i]
        last_number = next_number
    return last_number


print(f"Part One: {find_number(INPUT, 2020)}")
print(f"Part Two: {find_number(INPUT, 30000000)}")

#!/usr/bin/env python3
from itertools import count
from operator import mul

with open("input.txt") as input_file:
    INPUT = ["".join(c for c in l.strip()) for l in input_file]


def more_zeroes(report, i):
    zeroes = sum(1 for line in report if line[i] == "0")
    ones = sum(1 for line in report if line[i] == "1")
    return zeroes > ones


def energy_consumption(report):
    gamma = ""
    epsilon = ""
    for i in range(len(report[0])):
        if more_zeroes(report, i):
            gamma += "0"
            epsilon += "1"
        else:
            gamma += "1"
            epsilon += "0"
    return int(gamma, 2), int(epsilon, 2)


def life_support(report):
    oxygen, co2 = report[:], report[:]
    for i in count():
        i %= len(report[0])
        if more_zeroes(oxygen, i):
            oxygen = [line for line in oxygen if line[i] == "0"]
        else:
            oxygen = [line for line in oxygen if line[i] == "1"]
        if len(oxygen) <= 1:
            break

    for i in count():
        i %= len(report[0])
        if more_zeroes(co2, i):
            co2 = [line for line in co2 if line[i] == "1"]
        else:
            co2 = [line for line in co2 if line[i] == "0"]
        if len(co2) <= 1:
            break

    return int(oxygen[0], 2), int(co2[0], 2)


print(f"Part One: {mul(*energy_consumption(INPUT))}")
print(f"Part Two: {mul(*life_support(INPUT))}")

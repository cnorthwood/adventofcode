#!/usr/bin/env python3

def load_calories(filename):
    elves = []
    this_elf = 0
    with open(filename) as input_file:
        for line in input_file:
            if not line.strip():
                elves.append(this_elf)
                this_elf = 0
            else:
                this_elf += int(line)
    if this_elf:
        elves.append(this_elf)
    return elves


ELF_CALORIES = sorted(load_calories("input.txt"))
print(f"Part One: {ELF_CALORIES[-1]}")
print(f"Part Two: {sum(ELF_CALORIES[-3:])}")

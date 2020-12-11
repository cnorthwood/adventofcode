#!/usr/bin/env python3

with open("input.txt") as input_file:
    INPUT = []
    for line in input_file:
        line_parts = line.split()
        INPUT.append((line_parts[0], int(line_parts[1])))


def find_loop(program):
    seen = set()
    acc = 0
    pc = 0
    while True:
        if pc in seen:
            return acc, False
        if pc >= len(program):
            return acc, True
        seen.add(pc)
        instruction, val = program[pc]
        if instruction == "nop":
            pc += 1
        elif instruction == "jmp":
            pc += val
        elif instruction == "acc":
            acc += val
            pc += 1
        else:
            raise ValueError(f"unrecognised instruction on line {pc}: {instruction}")


def generate_variants(program):
    for i in range(len(program)):
        if program[i][0] == "nop":
            yield program[:i] + [("jmp", program[i][1])] + program[i+1:]
        if program[i][0] == "jmp":
            yield program[:i] + [("nop", program[i][1])] + program[i+1:]


print(f"Part One: {find_loop(INPUT)[0]}")
for variant in generate_variants(INPUT):
    acc, result = find_loop(variant)
    if result:
        print(f"Part Two: {acc}")
        break

#!/usr/bin/env python3

from itertools import count


class Halt(Exception):
    pass


class IllegalOperationError(Exception):
    pass


def step(pc, program):
    if program[pc] == 1:
        program[program[pc + 3]] = program[program[pc + 1]] + program[program[pc + 2]]
    elif program[pc] == 2:
        program[program[pc + 3]] = program[program[pc + 1]] * program[program[pc + 2]]
    elif program[pc] == 99:
        raise Halt()
    else:
        raise IllegalOperationError()
    return program


def run(inital_program):
    program = list(inital_program)
    for pc in count(0, step=4):
        try:
            program = step(pc, program)
        except Halt:
            return program[0]


def patch_noun_verb(prog, noun, verb):
    prog = list(prog)
    prog[1] = noun
    prog[2] = verb
    return prog


with open("input.txt") as input_file:
    INPUT = [int(instruction) for instruction in input_file.read().split(",")]


def part_two(program):
    for noun in range(100):
        for verb in range(100):
            if run(patch_noun_verb(program, noun, verb)) == 19690720:
                return 100 * noun + verb


print(f"Part One: {run(patch_noun_verb(INPUT, 12, 2))}")
print(f"Part Two: {part_two(INPUT)}")

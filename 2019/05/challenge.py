#!/usr/bin/env pypy3

from collections import namedtuple

OUTPUTS = []


class Halt(Exception):
    pass


class IllegalOperationError(Exception):
    pass


def op_add(prog, pc, modes):
    prog[prog[pc + 3]] = mem_read(prog, pc + 1, modes[0]) + mem_read(prog, pc + 2, modes[1])
    return pc + 4


def op_mult(prog, pc, modes):
    prog[prog[pc + 3]] = mem_read(prog, pc + 1, modes[0]) * mem_read(prog, pc + 2, modes[1])
    return pc + 4


def op_input(prog, pc, modes):
    prog[prog[pc + 1]] = INPUT_VAL
    return pc + 2


def op_output(prog, pc, modes):
    OUTPUTS.append(mem_read(prog, pc + 1, modes[0]))
    return pc + 2


def op_jump_if_true(prog, pc, modes):
    if mem_read(prog, pc + 1, modes[0]) != 0:
        return mem_read(prog, pc + 2, modes[1])
    return pc + 3


def op_jump_if_false(prog, pc, modes):
    if mem_read(prog, pc + 1, modes[0]) == 0:
        return mem_read(prog, pc + 2, modes[1])
    return pc + 3


def op_less_than(prog, pc, modes):
    prog[prog[pc + 3]] = 1 if mem_read(prog, pc + 1, modes[0]) < mem_read(prog, pc + 2, modes[1]) else 0
    return pc + 4


def op_equals(prog, pc, modes):
    prog[prog[pc + 3]] = 1 if mem_read(prog, pc + 1, modes[0]) == mem_read(prog, pc + 2, modes[1]) else 0
    return pc + 4


def op_halt(prog, pc, modes):
    raise Halt()


Operation = namedtuple("Operation", ["f", "params"])
Opcode = namedtuple("Opcode", ["operation", "modes"])

OPERATIONS = {
    1: Operation(
        f=op_add,
        params=3,
    ),
    2: Operation(
        f=op_mult,
        params=3,
    ),
    3: Operation(
        f=op_input,
        params=1,
    ),
    4: Operation(
        f=op_output,
        params=1,
    ),
    5: Operation(
        f=op_jump_if_true,
        params=2,
    ),
    6: Operation(
        f=op_jump_if_false,
        params=2,
    ),
    7: Operation(
        f=op_less_than,
        params=2,
    ),
    8: Operation(
        f=op_equals,
        params=2,
    ),
    99: Operation(
        f=op_halt,
        params=0,
    ),
}


def mem_read(prog, address, mode):
    if mode == 0:
        return prog[prog[address]]
    elif mode == 1:
        return prog[address]
    else:
        raise IllegalOperationError()


def parse_opcode(opcode):
    operation = OPERATIONS[opcode % 100]
    modes = []
    for i in range(operation.params):
        modes.append((opcode // (10 ** (2 + i))) % 10)
    return Opcode(operation=operation.f, modes=modes)


def step(pc, program):
    opcode = parse_opcode(program[pc])
    return opcode.operation(program, pc, opcode.modes)


def run(inital_program):
    OUTPUTS.clear()
    program = list(inital_program)
    pc = 0
    while True:
        try:
            pc = step(pc, program)
        except Halt:
            return OUTPUTS


with open("input.txt") as input_file:
    INPUT = [int(instruction) for instruction in input_file.read().split(",")]

INPUT_VAL = 1
print(f"Part One: {''.join(str(output) for output in run(INPUT) if output > 0)}")
INPUT_VAL = 5
print(f"Part Two: {''.join(str(output) for output in run(INPUT) if output > 0)}")

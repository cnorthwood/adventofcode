#!/usr/bin/env pypy3

from collections import namedtuple
from itertools import permutations
from threading import Thread
from queue import Queue


class Halt(Exception):
    pass


class IllegalOperationError(Exception):
    pass


def op_add(prog, pc, modes, inputs, outputs):
    prog[prog[pc + 3]] = mem_read(prog, pc + 1, modes[0]) + mem_read(prog, pc + 2, modes[1])
    return pc + 4


def op_mult(prog, pc, modes, inputs, outputs):
    prog[prog[pc + 3]] = mem_read(prog, pc + 1, modes[0]) * mem_read(prog, pc + 2, modes[1])
    return pc + 4


def op_input(prog, pc, modes, inputs, outputs):
    prog[prog[pc + 1]] = inputs.get()
    return pc + 2


def op_output(prog, pc, modes, inputs, outputs):
    outputs.put(mem_read(prog, pc + 1, modes[0]))
    return pc + 2


def op_jump_if_true(prog, pc, modes, inputs, outputs):
    if mem_read(prog, pc + 1, modes[0]) != 0:
        return mem_read(prog, pc + 2, modes[1])
    return pc + 3


def op_jump_if_false(prog, pc, modes, inputs, outputs):
    if mem_read(prog, pc + 1, modes[0]) == 0:
        return mem_read(prog, pc + 2, modes[1])
    return pc + 3


def op_less_than(prog, pc, modes, inputs, outputs):
    prog[prog[pc + 3]] = 1 if mem_read(prog, pc + 1, modes[0]) < mem_read(prog, pc + 2, modes[1]) else 0
    return pc + 4


def op_equals(prog, pc, modes, inputs, outputs):
    prog[prog[pc + 3]] = 1 if mem_read(prog, pc + 1, modes[0]) == mem_read(prog, pc + 2, modes[1]) else 0
    return pc + 4


def op_halt(prog, pc, modes, inputs, outputs):
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


def step(pc, program, inputs, outputs):
    opcode = parse_opcode(program[pc])
    return opcode.operation(program, pc, opcode.modes, inputs, outputs)


def run(inital_program, inputs, outputs):
    program = list(inital_program)
    pc = 0
    while True:
        try:
            pc = step(pc, program, inputs, outputs)
        except Halt:
            return


with open("input.txt") as input_file:
    INPUT = [int(instruction) for instruction in input_file.read().split(",")]


def test_configuration(program, phases):
    inputs_a = Queue()
    inputs_a.put(phases[0])
    inputs_a.put(0)
    outputs_a = Queue()
    run(program, inputs_a, outputs_a)
    inputs_b = Queue()
    inputs_b.put(phases[1])
    inputs_b.put(outputs_a.get())
    outputs_b = Queue()
    run(program, inputs_b, outputs_b)
    inputs_c = Queue()
    inputs_c.put(phases[2])
    inputs_c.put(outputs_b.get())
    outputs_c = Queue()
    run(program, inputs_c, outputs_c)
    inputs_d = Queue()
    inputs_d.put(phases[3])
    inputs_d.put(outputs_c.get())
    outputs_d = Queue()
    run(program, inputs_d, outputs_d)
    inputs_e = Queue()
    inputs_e.put(phases[4])
    inputs_e.put(outputs_d.get())
    outputs_e = Queue()
    run(program, inputs_e, outputs_e)
    return outputs_e.get()


def feedback_loop(program, phases):
    qea = Queue()
    qea.put(phases[0])
    qea.put(0)
    qab = Queue()
    qab.put(phases[1])
    qbc = Queue()
    qbc.put(phases[2])
    qcd = Queue()
    qcd.put(phases[3])
    qde = Queue()
    qde.put(phases[4])
    threads = [
        Thread(name="Amp-A", target=run, args=(program, qea, qab)),
        Thread(name="Amp-B", target=run, args=(program, qab, qbc)),
        Thread(name="Amp-C", target=run, args=(program, qbc, qcd)),
        Thread(name="Amp-D", target=run, args=(program, qcd, qde)),
        Thread(name="Amp-E", target=run, args=(program, qde, qea)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return qea.get()



print(f"Part One: {max(test_configuration(INPUT, phases) for phases in permutations(range(5)))}")
print(f"Part Two: {max(feedback_loop(INPUT, phases) for phases in permutations(range(5, 10)))}")

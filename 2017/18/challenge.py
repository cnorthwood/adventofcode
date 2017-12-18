#!/usr/bin/env pypy3

from collections import defaultdict


def execute(instructions):
    registers = defaultdict(int)
    sounds = []

    def deref(x):
        try:
            return int(x)
        except:
            return registers[x]

    def snd(x):
        sounds.append(deref(x))
        return None, 1

    def set(x, y):
        registers[x] = deref(y)
        return None, 1

    def add(x, y):
        registers[x] += deref(y)
        return None, 1

    def mul(x, y):
        registers[x] *= deref(y)
        return None, 1

    def mod(x, y):
        registers[x] %= deref(y)
        return None, 1

    def rcv(x):
        if deref(x) != 0:
            return sounds[-1], 1
        else:
            return None, 1

    def jgz(x, y):
        if deref(x) > 0:
            return None, deref(y)
        else:
            return None, 1

    ops = {
        'snd': snd,
        'set': set,
        'add': add,
        'mul': mul,
        'mod': mod,
        'rcv': rcv,
        'jgz': jgz,
    }

    asm = []
    for instruction in instructions.strip().splitlines():
        parts = instruction.split()
        asm.append((parts[0], parts[1:]))

    pc = 0
    recovered = None
    while recovered is None and 0 <= pc < len(asm):
        op, args = asm[pc]
        recovered, jump = ops[op](*args)
        pc += jump
    return recovered


TEST = """
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
"""

assert execute(TEST) == 4
with open('input.txt') as input_file:
    INPUT = input_file.read().strip()

print("Part One:", execute(INPUT))

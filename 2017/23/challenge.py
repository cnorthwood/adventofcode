#!/usr/bin/env pypy3

from itertools import product


def execute(instructions):
    registers = {r: 0 for r in 'abcdefgh'}

    def deref(x):
        try:
            return int(x)
        except:
            return registers[x]

    def set(x, y):
        registers[x] = deref(y)
        return 1

    def sub(x, y):
        registers[x] -= deref(y)
        return 1

    def mul(x, y):
        registers[x] *= deref(y)
        return 1

    def jnz(x, y):
        if deref(x) != 0:
            return deref(y)
        else:
            return 1

    ops = {
        'set': set,
        'sub': sub,
        'mul': mul,
        'jnz': jnz,
    }

    asm = []
    for instruction in instructions.strip().splitlines():
        parts = instruction.split()
        asm.append((parts[0], parts[1:]))

    pc = 0
    mul_count = 0
    while 0 <= pc < len(asm):
        op, args = asm[pc]
        if op == 'mul':
            mul_count += 1
        jump = ops[op](*args)
        pc += jump
    return mul_count


with open('input.txt') as input_file:
    INPUT = input_file.read().strip()

print("Part One:", execute(INPUT))


def main():
    h = 0
    for b in range(109900, 126901, 17):
        for d in range(2, int(b**0.5)+1):
            if b % d == 0:
                h += 1
                break
    return h

print("Part Two:", main())

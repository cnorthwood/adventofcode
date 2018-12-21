#!/usr/bin/env pypy3
from itertools import count


def addr(r, in1, in2, out):
    r[out] = r[in1] + r[in2]


def addi(r, in1, in2, out):
    r[out] = r[in1] + in2


def mulr(r, in1, in2, out):
    r[out] = r[in1] * r[in2]


def muli(r, in1, in2, out):
    r[out] = r[in1] * in2


def banr(r, in1, in2, out):
    r[out] = r[in1] & r[in2]


def bani(r, in1, in2, out):
    r[out] = r[in1] & in2


def borr(r, in1, in2, out):
    r[out] = r[in1] | r[in2]


def bori(r, in1, in2, out):
    r[out] = r[in1] | in2


def setr(r, in1, in2, out):
    r[out] = r[in1]


def seti(r, in1, in2, out):
    r[out] = in1


def gtir(r, in1, in2, out):
    r[out] = 1 if in1 > r[in2] else 0


def gtri(r, in1, in2, out):
    r[out] = 1 if r[in1] > in2 else 0


def gtrr(r, in1, in2, out):
    r[out] = 1 if r[in1] > r[in2] else 0


def eqir(r, in1, in2, out):
    r[out] = 1 if in1 == r[in2] else 0


def eqri(r, in1, in2, out):
    r[out] = 1 if r[in1] == in2 else 0


def eqrr(r, in1, in2, out):
    r[out] = 1 if r[in1] == r[in2] else 0


OPS = {
    'addr': addr,
    'addi': addi,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr,
}


def load_prog(filename):
    with open(filename) as input_file:
        lines = input_file.read().strip().splitlines()
    ip_line, prog_lines = lines[0], lines[1:]
    assert(ip_line.startswith('#ip'))
    ip = int(ip_line.split()[1])
    prog = []
    for line in prog_lines:
        line = line.split()
        op, args = OPS[line[0]], [int(a) for a in line[1:]]
        prog.append((op, args))
    return ip, prog


class InfiniteLoopException(Exception):
    pass


def execute(ipr, instructions, initial_r0=0):
    r = [initial_r0] + [0] * 5
    while 0 <= r[ipr] < len(instructions):
        op, args = instructions[r[ipr]]
        if op not in {setr, seti} and args[0] == 0 or args[1] == 0:
            return r
        op(r, *args)
        r[ipr] += 1
    r[ipr] -= 1
    return r


IP, PROG = load_prog('input.txt')


def part_one(ipr, instructions):
    r = [0] * 6
    while 0 <= r[ipr] < len(instructions):
        op, args = instructions[r[ipr]]
        # break when r0 is looked at
        if op in {gtri, eqri, gtrr, eqrr} and args[0] == 0:
            return r[args[1]]
        if op in {gtir, eqir, gtrr, eqrr} and args[1] == 0:
            return r[args[0]]
        op(r, *args)
        r[ipr] += 1
    r[ipr] -= 1
    return r


print("Part One: {}".format(part_one(IP, PROG)))

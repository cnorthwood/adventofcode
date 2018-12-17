#!/usr/bin/env pypy3

import re


INPUT_RE = re.compile(r'(?:Before|After):\s+\[(\d), (\d), (\d), (\d)\]')


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


POTENTIAL_OPCODES = frozenset({
    addr, addi,
    mulr, muli,
    banr, bani,
    borr, bori,
    setr, seti,
    gtir, gtri, gtrr,
    eqir, eqri, eqrr,
})


def determine_possibilities(input, args, expected, opcodes=POTENTIAL_OPCODES):
    poss = set()
    for op in opcodes:
        registers = list(input)
        op(registers, *args)
        if registers == expected:
            poss.add(op)
    return poss


assert(len(list(determine_possibilities([3, 2, 1, 1], [2, 1, 2], [3, 2, 2, 1]))) == 3)


def parse_list(line):
    match = INPUT_RE.match(line)
    return [int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))]


def parse_input(filename):
    with open(filename) as input_file:
        data = input_file.read().strip()
    sample_lines, test_prog = data.split('\n\n\n')
    samples = []
    for sample in sample_lines.split('\n\n'):
        before, instr, after = sample.split('\n')
        before = parse_list(before)
        instr = list(map(int, instr.split()))
        after = parse_list(after)
        samples.append((before, instr, after))
    test_prog = [list(map(int, line.split())) for line in test_prog.strip().splitlines()]
    return samples, test_prog


def part_one(samples):
    return sum(1 for before, instructions, after in samples if len(list(determine_possibilities(before, instructions[1:], after))) >= 3)


SAMPLES, TEST_PROG = parse_input('input.txt')

print("Part One: {}".format(part_one(SAMPLES)))


def determine_opcodes(samples):
    potential_opcodes = {i: set(POTENTIAL_OPCODES) for i in range(len(POTENTIAL_OPCODES))}
    opcodes = {i: None for i in range(len(POTENTIAL_OPCODES))}
    for before, (op, a, b, c), after in samples:
        potential_opcodes[op] = determine_possibilities(before, (a, b, c), after, potential_opcodes[op])
        if len(potential_opcodes[op]) == 1:
            opcodes[op] = potential_opcodes[op].pop()
            for other_op in potential_opcodes:
                potential_opcodes[other_op] -= {opcodes[op]}
    assert(all(f is not None for op, f in opcodes.items()))
    return opcodes


def execute(opcodes, instructions):
    r = [0] * 4
    for op, a, b, c in instructions:
        opcodes[op](r, a, b, c)
    return r


print("Part Two: {}".format(execute(determine_opcodes(SAMPLES), TEST_PROG)[0]))

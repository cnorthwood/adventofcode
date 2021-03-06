#!/usr/bin/env pypy3


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


def execute(ipr, instructions, initial_r0=0):
    r = [initial_r0] + [0] * 5
    while 0 <= r[ipr] < len(instructions):
        # optimiser hack, stolen from Reddit
        if r[ipr] == 1:
            range_reg = max(enumerate(r), key=lambda reg: reg[1])[0]
            r[0] = sum(i for i in range(1, r[range_reg] + 1) if r[range_reg] % i == 0)
            break
        op, args = instructions[r[ipr]]
        op(r, *args)
        r[ipr] += 1
    r[ipr] -= 1
    return r


# TEST_IP, TEST_PROG = load_prog('test.txt')
IP, PROG = load_prog('input.txt')
# assert(execute(TEST_IP, TEST_PROG) == [6, 5, 6, 0, 0, 9])
print("Part One: {}".format(execute(IP, PROG)[0]))
print("Part Two: {}".format(execute(IP, PROG, 1)[0]))

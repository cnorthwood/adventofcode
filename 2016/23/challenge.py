REGISTERS = {
    'a': 12,
    'b': 0,
    'c': 0,
    'd': 0,
}


def isdigit(x):
    try:
        int(x)
    except ValueError:
        return False
    else:
        return True


def deref(x):
    if isdigit(x):
        return int(x)
    else:
        return REGISTERS[x]


def cpy(x, y):
    if y in REGISTERS:
        REGISTERS[y] = deref(x)
    return 1


def inc(x):
    REGISTERS[x] += 1
    return 1


def dec(x):
    REGISTERS[x] -= 1
    return 1


def jnz(x, y):
    if deref(x) == 0:
        return 1
    else:
        return deref(y)


def tgl(x):
    t = pc + deref(x)
    if t >= 0 and t < len(INSTRUCTIONS):
        if INSTRUCTIONS[t][0] == inc:
            INSTRUCTIONS[t] = (dec, INSTRUCTIONS[t][1])
        elif INSTRUCTIONS[t][0] in (dec, tgl):
            INSTRUCTIONS[t] = (inc, INSTRUCTIONS[t][1])
        elif INSTRUCTIONS[t][0] == jnz:
            INSTRUCTIONS[t] = (cpy, INSTRUCTIONS[t][1])
        elif INSTRUCTIONS[t][0] == cpy:
            INSTRUCTIONS[t] = (jnz, INSTRUCTIONS[t][1])
    return 1


def mult_lookahead(instructions):
    if [op for op, args in instructions] == [inc, dec, jnz, dec, jnz]:
        reg_a = instructions[1][1][0]
        reg_b = instructions[3][1][0]
        if instructions[2][1][0] == reg_a and instructions[4][1][0] == reg_b:
            return True
    return False


def mult_opt(*instructions):
    target = instructions[0][1][0]
    reg_a = instructions[1][1][0]
    reg_b = instructions[3][1][0]
    REGISTERS[target] += REGISTERS[reg_a] * REGISTERS[reg_b]
    REGISTERS[reg_a] = 0
    REGISTERS[reg_b] = 0
    return 4

OPS = {
    'cpy': cpy,
    'inc': inc,
    'dec': dec,
    'jnz': jnz,
    'tgl': tgl,
}

INSTRUCTIONS = []
with open('input.txt') as input:
    for line in input:
        parts = line.split()
        INSTRUCTIONS.append((OPS[parts[0]], parts[1:]))
pc = 0

while pc < len(INSTRUCTIONS):
    op, args = INSTRUCTIONS[pc]
    if mult_lookahead(INSTRUCTIONS[pc:pc+5]):
        op, args = mult_opt, INSTRUCTIONS[pc:pc+5]
    pc += op(*args)

print "Part Two:", REGISTERS['a']

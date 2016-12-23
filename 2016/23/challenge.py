REGISTERS = {
    'a': 7,
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
    pc += op(*args)

print "Part One:", REGISTERS['a']

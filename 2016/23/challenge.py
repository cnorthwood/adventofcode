REGISTERS = {
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0,
}

def deref(x):
    if x.isdigit():
        return int(x)
    else:
        return REGISTERS[x]


def cpy(x, y):
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
        return int(y)

OPS = {
    'cpy': cpy,
    'inc': inc,
    'dec': dec,
    'jnz': jnz,
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

registers = {'a': 1, 'b': 0}

def hlf(r):
    registers[r] /= 2
    return 1

def tpl(r):
    registers[r] *= 3
    return 1

def inc(r):
    registers[r] += 1
    return 1

def jmp(offset):
    return int(offset)

def jie(r, offset):
    if registers[r] % 2 == 0:
        return int(offset)
    else:
        return 1

def jio(r, offset):
    if registers[r] == 1:
        return int(offset)
    else:
        return 1

ops = {
    'hlf': hlf,
    'tpl': tpl,
    'inc': inc,
    'jmp': jmp,
    'jie': jie,
    'jio': jio
}

INSTRUCTIONS = """jio a, +19
inc a
tpl a
inc a
tpl a
inc a
tpl a
tpl a
inc a
inc a
tpl a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
jmp +23
tpl a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
inc a
tpl a
inc a
tpl a
inc a
tpl a
inc a
inc a
tpl a
inc a
inc a
tpl a
tpl a
inc a
jio a, +8
inc b
jie a, +4
tpl a
inc a
jmp +2
hlf a
jmp -7""".splitlines()

pc = 0

while True:
    try:
        op, args = INSTRUCTIONS[pc].split(None, 1)
        args = args.split(', ')
        pc += ops[op](*args)
    except IndexError:
        break

print registers['b']

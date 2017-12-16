#!/usr/bin/env pypy3


def spin(l, x):
    return l[-x:] + l[:len(l) - x]


def exchange(l, a, b):
    new_l = list(l)
    new_l[a], new_l[b] = l[b], l[a]
    return ''.join(new_l)


def partner(l, a, b):
    return l.translate(str.maketrans(f'{a}{b}', f'{b}{a}'))


assert spin('abcde', 3) == 'cdeab'
assert spin('abcde', 1) == 'eabcd'
assert exchange('eabcd', 3, 4) == 'eabdc'
assert partner('eabdc', 'e', 'b') == 'baedc'


def parse(input):
    l = 'abcdefghijklmnop'
    for command in input.split(','):
        if command[0] == 's':
            l = spin(l, int(command[1:]))
        elif command[0] == 'x':
            args = command[1:].split('/')
            l = exchange(l, int(args[0]), int(args[1]))
        elif command[0] == 'p':
            args = command[1:].split('/')
            l = partner(l, args[0], args[1])
        else:
            raise Exception('unrecognised command')
    return l


with open('input.txt') as input_file:
    INPUT = input_file.read().strip()
print("Part One:", parse(INPUT))

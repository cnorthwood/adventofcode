#!/usr/bin/env pypy3

from collections import defaultdict


def build_processor(write0, move0, next0, write1, move1, next1):
    def processor(tape, cursor):
        if tape[cursor] == 0:
            tape[cursor] = write0
            if move0 == 'right':
                return cursor + 1, next0
            else:
                return cursor - 1, next0
        else:
            tape[cursor] = write1
            if move1 == 'right':
                return cursor + 1, next1
            else:
                return cursor - 1, next1
    return processor


def parse(input):
    lines = input.splitlines()
    begin = lines[0].split()[-1].strip('.')
    diagnostic = int(lines[1].split()[-2])

    processors = {}
    for start_line in range(3, len(lines), step=10):
        state_name = lines[start_line].split()[-1].strip(':')
        write0 = int(lines[start_line+2].split()[-1].strip('.'))
        move0 = lines[start_line+3].split()[-1].strip('.')
        next0 = lines[start_line+4].split()[-1].strip('.')
        write1 = int(lines[start_line+6].split()[-1].strip('.'))
        move1 = lines[start_line+7].split()[-1].strip('.')
        next1 = lines[start_line+8].split()[-1].strip('.')
        processors[state_name] = build_processor(write0, move0, next0, write1, move1, next1)

    return begin, diagnostic, processors


with open('input.txt') as input_file:
    state, steps, processors = parse(input_file.read())


TAPE = defaultdict(int)
cursor = 0
for _ in range(steps):
    cursor, state = processors[state](TAPE, cursor)
print("Part One:", sum(TAPE.values()))

#!/usr/bin/env python3

from collections import defaultdict
import re

INPUT_RE = re.compile(r'(?P<register>\w+) (?P<operation>dec|inc) (?P<value>-?\d+) if (?P<test_register>\w+) (?P<test_operation><|<=|>|>=|==|!=) (?P<test_value>-?\d+)')

OPERATIONS = {
    '==': lambda registers, register, value: registers[register] == value,
    '>': lambda registers, register, value: registers[register] > value,
    '>=': lambda registers, register, value: registers[register] >= value,
    '<': lambda registers, register, value: registers[register] < value,
    '<=': lambda registers, register, value: registers[register] <= value,
    '!=': lambda registers, register, value: registers[register] != value,
}


def process(registers, register, operation, val, test_register, test_operation, test_value):
    if OPERATIONS[test_operation](registers, test_register, test_value):
        if operation == 'inc':
            registers[register] += val
        if operation == 'dec':
            registers[register] -= val


def largest(registers):
    return max(registers.values())


test_registers = defaultdict(int)

process(test_registers, 'b', 'inc', 5, 'a', '>', 1)
assert test_registers['b'] == 0

process(test_registers, 'a', 'inc', 1, 'b', '<', 5)
assert test_registers['a'] == 1

process(test_registers, 'c', 'dec', -10, 'a', '>=', 1)
assert test_registers['c'] == 10

process(test_registers, 'c', 'inc', -20, 'c', '==', 10)
assert test_registers['c'] == -10

assert largest(test_registers) == 1

registers = defaultdict(int)
largest_values = set()

with open('input.txt') as input:
    for line in input:
        match = INPUT_RE.match(line)
        process(
            registers,
            match.group('register'),
            match.group('operation'),
            int(match.group('value')),
            match.group('test_register'),
            match.group('test_operation'),
            int(match.group('test_value')),
        )
        largest_values.add(largest(registers))


print("Part One:", largest(registers))
print("Part Two:", max(largest_values))

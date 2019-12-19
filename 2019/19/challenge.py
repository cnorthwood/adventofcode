#!/usr/bin/env pypy3

from collections import defaultdict, namedtuple
from functools import lru_cache
import sys


class Halt(Exception):
    pass


class IllegalOperationError(Exception):
    pass


Operation = namedtuple("Operation", ["f", "params"])
Opcode = namedtuple("Opcode", ["operation", "modes"])


class IntcodeVM:
    def __init__(self, program, input_reader, output_writer):
        self._memory = defaultdict(int)
        for i, data in enumerate(program):
            self._memory[i] = data
        self._pc = 0
        self._relative_base = 0
        self._input_reader = input_reader
        self._output_writer = output_writer
        self._OPERATIONS = {
            1: Operation(
                f=self._op_add,
                params=3,
            ),
            2: Operation(
                f=self._op_mult,
                params=3,
            ),
            3: Operation(
                f=self._op_input,
                params=1,
            ),
            4: Operation(
                f=self._op_output,
                params=1,
            ),
            5: Operation(
                f=self._op_jump_if_true,
                params=2,
            ),
            6: Operation(
                f=self._op_jump_if_false,
                params=2,
            ),
            7: Operation(
                f=self._op_less_than,
                params=3,
            ),
            8: Operation(
                f=self._op_equals,
                params=3,
            ),
            9: Operation(
                f=self._op_adjust_relative_base,
                params=1,
            ),
            99: Operation(
                f=self._op_halt,
                params=0,
            ),
        }

    def _op_add(self, modes):
        self._mem_write(self._memory[self._pc + 3], modes[2],
                        self._mem_read(self._pc + 1, modes[0]) + self._mem_read(self._pc + 2, modes[1]))
        self._pc += 4

    def _op_mult(self, modes):
        self._mem_write(self._memory[self._pc + 3], modes[2],
                        self._mem_read(self._pc + 1, modes[0]) * self._mem_read(self._pc + 2, modes[1]))
        self._pc += 4

    def _op_input(self, modes):
        self._mem_write(self._memory[self._pc + 1], modes[0], self._input_reader())
        self._pc += 2

    def _op_output(self, modes):
        self._output_writer(self._mem_read(self._pc + 1, modes[0]))
        self._pc += 2

    def _op_jump_if_true(self, modes):
        if self._mem_read(self._pc + 1, modes[0]) != 0:
            self._pc = self._mem_read(self._pc + 2, modes[1])
        else:
            self._pc += 3

    def _op_jump_if_false(self, modes):
        if self._mem_read(self._pc + 1, modes[0]) == 0:
            self._pc = self._mem_read(self._pc + 2, modes[1])
        else:
            self._pc += 3

    def _op_less_than(self, modes):
        self._mem_write(self._memory[self._pc + 3], modes[2],
                        1 if self._mem_read(self._pc + 1, modes[0]) < self._mem_read(self._pc + 2, modes[1]) else 0)
        self._pc += 4

    def _op_equals(self, modes):
        self._mem_write(self._memory[self._pc + 3], modes[2],
                        1 if self._mem_read(self._pc + 1, modes[0]) == self._mem_read(self._pc + 2, modes[1]) else 0)
        self._pc += 4

    def _op_adjust_relative_base(self, modes):
        self._relative_base += self._mem_read(self._pc + 1, modes[0])
        self._pc += 2

    def _op_halt(self, modes):
        raise Halt()

    def _mem_read(self, address, mode):
        if mode == 0:
            return self._memory[self._memory[address]]
        elif mode == 1:
            return self._memory[address]
        elif mode == 2:
            return self._memory[self._relative_base + self._memory[address]]
        else:
            raise IllegalOperationError()

    def _mem_write(self, address, mode, val):
        if mode == 0:
            self._memory[address] = val
        elif mode == 2:
            self._memory[self._relative_base + address] = val
        else:
            raise IllegalOperationError()

    def _parse_opcode(self, opcode):
        operation = self._OPERATIONS[opcode % 100]
        modes = []
        for i in range(operation.params):
            modes.append((opcode // (10 ** (2 + i))) % 10)
        return Opcode(operation=operation.f, modes=modes)

    def run(self):
        while True:
            opcode = self._parse_opcode(self._memory[self._pc])
            try:
                opcode.operation(opcode.modes)
            except Halt:
                return


@lru_cache(maxsize=None)
def is_in_range(x, y):
    input = [y, x]
    output = []
    IntcodeVM(PROGRAM, input.pop, output.append).run()
    return sum(output)


def find_points(width=50, height=50):
    return {(x, y): is_in_range(x, y) for x in range(width) for y in range(height)}

def get_beam_width(d):
    # Assume beam is between 22.5-67.5º
    return sum(is_in_range(x, d) for x in range(d * 2))


def get_beam_height(d):
    # Assume beam is between 22.5-67.5º
    return sum(is_in_range(d, y) for y in range(d * 2))


def get_start(f):
    bottom = 0
    top = 10000
    while bottom <= top:
        mid = (bottom + top) // 2
        r = f(mid)
        if r < 100:
            bottom = mid + 1
        elif r > 100:
            top = mid - 1
        else:
            return mid


def is_square(top_left_x, top_left_y, size=100):
    return all(is_in_range(x, y) == 1 for x in range(top_left_x, top_left_x + size) for y in range(top_left_y, top_left_y + size))


def part_two():
    start_x = get_start(get_beam_height)
    start_y = get_start(get_beam_width)
    for x in range(start_x, start_x + 1000):
        for y in range(start_y, start_y + 1000):
            if is_square(x, y):
                return x, y


with open("input.txt") as input_file:
    PROGRAM = [int(instruction) for instruction in input_file.read().split(",")]

POINTS = find_points()
print(f"Part One: {sum(POINTS.values())}")
# for y in range(50):
#     for x in range(50):
#         sys.stdout.write("#" if POINTS[x, y] == 1 else ".")
#     sys.stdout.write("\n")

SQUARE = part_two()
print(f"Part Two: {SQUARE[0] * 10000 + SQUARE[1]}")
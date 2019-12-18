#!/usr/bin/env pypy3

from collections import defaultdict, namedtuple


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


def null_input():
    raise IOError()


def build_map(program):
    output = []
    IntcodeVM(program, null_input, output.append).run()
    return {(x, y): d for y, line in enumerate("".join(chr(d) for d in output).splitlines(keepends=False)) for x, d in enumerate(line)}


def find_intersections(map):
    max_x = max(x for x, y in map.keys())
    max_y = max(y for x, y in map.keys())
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if map.get((x, y), ".") == "#" \
                and map.get((x - 1, y), ".") == "#" \
                and map.get((x + 1, y), ".") == "#" \
                and map.get((x, y - 1), ".") == "#" \
                and map.get((x, y + 1), ".") == "#":
                yield x * y


with open("input.txt") as input_file:
    INPUT = [int(instruction) for instruction in input_file.read().split(",")]

MAP = build_map(INPUT)
print(f"Part One: {sum(find_intersections(MAP))}")

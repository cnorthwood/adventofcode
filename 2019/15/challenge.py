#!/usr/bin/env pypy3

from collections import defaultdict, deque, namedtuple

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

HIT_WALL = 0
MOVED = 1
FOUND_OXYGEN = 2


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

    def clone(self, input_reader, output_reader):
        clone = IntcodeVM([], input_reader, output_reader)
        clone._pc = self._pc
        clone._relative_base = self._relative_base
        for address, value in self._memory.items():
            clone._memory[address] = value
        return clone


def step(last, direction):
    def inputs():
        if inputs.called:
            raise Halt()
        inputs.called = True
        return direction
    inputs.called = False
    output = deque()
    vm = last.clone(inputs, output.append)
    vm.run()
    return vm, output.popleft()


def search(program):
    repair_map = {}
    bfs_q = deque()
    bfs_q.append((IntcodeVM(program, None, None), (0, 0), 0))
    o2_found = None
    while bfs_q:
        current_vm, (x, y), steps = bfs_q.popleft()
        for direction in [NORTH, SOUTH, EAST, WEST]:
            if direction == NORTH:
                next_pos = (x, y - 1)
            elif direction == SOUTH:
                next_pos = (x, y + 1)
            elif direction == EAST:
                next_pos = (x + 1, y)
            elif direction == WEST:
                next_pos = (x - 1, y)
            if next_pos not in repair_map:
                next_vm, output = step(current_vm, direction)
                repair_map[next_pos] = output
                if output == FOUND_OXYGEN and not o2_found:
                    o2_found = steps + 1
                if output != HIT_WALL:
                    bfs_q.append((next_vm, next_pos, steps + 1))
    return o2_found, repair_map


def simulate_o2_fill(repair_map):
    visited = set()
    x, y = next(pos for pos, content in repair_map.items() if content == FOUND_OXYGEN)
    bfs_q = deque()
    bfs_q.append(((x, y), 0))
    minutes = 0
    while bfs_q:
        (x, y), steps = bfs_q.popleft()
        visited.add((x, y))
        minutes = max(minutes, steps)
        for direction in [NORTH, SOUTH, EAST, WEST]:
            if direction == NORTH:
                next_pos = (x, y - 1)
            elif direction == SOUTH:
                next_pos = (x, y + 1)
            elif direction == EAST:
                next_pos = (x + 1, y)
            elif direction == WEST:
                next_pos = (x - 1, y)
            if repair_map[next_pos] == MOVED and next_pos not in visited:
                bfs_q.append((next_pos, steps + 1))
    return minutes


with open("input.txt") as input_file:
    INPUT = [int(instruction) for instruction in input_file.read().split(",")]


PART_ONE, MAP = search(INPUT)
print(f"Part One: {PART_ONE}")
print(f"Part Two: {simulate_o2_fill(MAP)}")
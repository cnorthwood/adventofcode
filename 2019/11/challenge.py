#!/usr/bin/env python3
# coding=utf8

from collections import defaultdict, namedtuple
from queue import Queue
import sys
from threading import Thread

BLACK = 0
WHITE = 1


class Halt(Exception):
    pass


class IllegalOperationError(Exception):
    pass


Operation = namedtuple("Operation", ["f", "params"])
Opcode = namedtuple("Opcode", ["operation", "modes"])


class IntcodeVM:
    def __init__(self, program, inputs, outputs):
        self._memory = defaultdict(int)
        for i, data in enumerate(program):
            self._memory[i] = data
        self._pc = 0
        self._relative_base = 0
        self.inputs = inputs
        self.outputs = outputs
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
        self._mem_write(self._memory[self._pc + 1], modes[0], self.inputs.get())
        self._pc += 2

    def _op_output(self, modes):
        self.outputs.put(self._mem_read(self._pc + 1, modes[0]))
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


def world_sim(world, inputs, outputs):
    direction = "U"
    x = 0
    y = 0
    while True:
        inputs.put(world.get((x, y), BLACK))
        world[x, y] = outputs.get()
        if direction == "U":
            direction = "L" if outputs.get() == 0 else "R"
        elif direction == "D":
            direction = "R" if outputs.get() == 0 else "L"
        elif direction == "R":
            direction = "U" if outputs.get() == 0 else "D"
        elif direction == "L":
            direction = "D" if outputs.get() == 0 else "U"
        if direction == "U":
            y -= 1
        elif direction == "D":
            y += 1
        elif direction == "L":
            x -= 1
        elif direction == "R":
            x += 1



def main(program, start_panel=BLACK):
    world = {(0,0): start_panel}
    inputs = Queue()
    outputs = Queue()
    vm = IntcodeVM(program, inputs, outputs)
    vm_thread = Thread(name="VM", target=vm.run)
    world_thread = Thread(name="World", target=world_sim, args=(world, inputs, outputs))
    world_thread.daemon = True
    vm_thread.start()
    world_thread.start()
    vm_thread.join()
    return world


with open("input.txt") as input_file:
    INPUT = [int(instruction) for instruction in input_file.read().split(",")]

print(f"Part One: {len(main(INPUT).keys())}")
world = main(INPUT, start_panel=WHITE)
points = {point for point, colour in world.items() if colour == WHITE}
min_x = min(point[0] for point in points) - 1
min_y = min(point[1] for point in points) - 1
max_x = max(point[0] for point in points) + 1
max_y = max(point[1] for point in points) + 1

print("Part Two:")
for y in range(min_y, max_y):
    for x in range(min_x, max_x):
        sys.stdout.write("█" if (x, y) in points else " ")
    sys.stdout.write("\n")
sys.stdout.write("\n")


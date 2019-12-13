#!/usr/bin/env pypy3

from collections import defaultdict, namedtuple
from queue import Queue
from threading import Thread

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4


class Halt(Exception):
    pass


class IllegalOperationError(Exception):
    pass


Operation = namedtuple("Operation", ["f", "params"])
Opcode = namedtuple("Opcode", ["operation", "modes"])


class IntcodeVM:
    def __init__(self, program, input_reader, output_writer):
        self._memory = defaultdict(int)
        self._vid_memory = {}
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


def num_blocks(display_mem):
    return sum(1 for tile in display_mem.values() if tile == BLOCK)


def ui(display_mem, outputs):
    while True:
        x = outputs.get()
        y = outputs.get()
        tile = outputs.get()
        display_mem[x, y] = tile
        outputs.task_done()
        outputs.task_done()
        outputs.task_done()


def find_ball(display_mem):
    pos = [(x, y) for (x, y), tile in display_mem.items() if tile == BALL]
    assert(len(pos) == 1)
    return pos[0]


def find_paddle(display_mem):
    pos = [(x, y) for (x, y), tile in display_mem.items() if tile == PADDLE]
    assert(len(pos) == 1)
    return pos[0]


def simulator(display_mem, wait_for_update):
    def simulate():
        wait_for_update()
        ball = find_ball(display_mem)
        paddle = find_paddle(display_mem)
        if ball[0] > paddle[0]:
            return 1
        elif ball[0] < paddle[0]:
            return -1
        else:
            return 0
    return simulate


def main(program, play):
    display_mem = {}
    outputs = Queue()
    if play:
        program[0] = 2
    vm = IntcodeVM(program, simulator(display_mem, outputs.join), outputs.put)
    vm_thread = Thread(name="VM", target=vm.run)
    ui_thread = Thread(name="UI", target=ui, args=(display_mem, outputs))
    ui_thread.daemon = True
    vm_thread.start()
    ui_thread.start()
    vm_thread.join()
    outputs.join()
    return display_mem


with open("input.txt") as input_file:
    INPUT = [int(instruction) for instruction in input_file.read().split(",")]

print(f"Part One: {num_blocks(main(INPUT, play=False))}")
print(f"Part Two: {main(INPUT, play=True)[-1, 0]}")

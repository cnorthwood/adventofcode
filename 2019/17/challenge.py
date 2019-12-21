#!/usr/bin/env pypy3

from collections import defaultdict, namedtuple
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


def find_start(map):
    return next(pos for pos, c in map.items() if c in "<>^v")


def find_path(map):
    x, y = find_start(map)
    direction = {"v": "D", "^": "U", "<": "L", ">": "R"}[map[x, y]]
    num_scaffold = sum(1 for c in map.values() if c == "#")
    visited = set()
    while len(visited) < num_scaffold:
        if direction == "D":
            next_pos = (x, y + 1)
        elif direction == "U":
            next_pos = (x, y - 1)
        elif direction == "L":
            next_pos = (x - 1, y)
        elif direction == "R":
            next_pos = (x + 1, y)
        if map.get(next_pos, ".") == "#":
            yield "1"
            x, y = next_pos
            visited.add(next_pos)
        else:
            if direction == "D" and map.get((x + 1, y), ".") == "#":
                yield "L"
                direction = "R"
            elif direction == "D" and map.get((x - 1, y), ".") == "#":
                yield "R"
                direction = "L"
            elif direction == "U" and map.get((x - 1, y), ".") == "#":
                yield "L"
                direction = "L"
            elif direction == "U" and map.get((x + 1, y), ".") == "#":
                yield "R"
                direction = "R"
            elif direction == "L" and map.get((x, y + 1), ".") == "#":
                yield "L"
                direction = "D"
            elif direction == "L" and map.get((x, y - 1), ".") == "#":
                yield "R"
                direction = "U"
            elif direction == "R" and map.get((x, y + 1), ".") == "#":
                yield "R"
                direction = "D"
            elif direction == "R" and map.get((x, y - 1), ".") == "#":
                yield "L"
                direction = "U"
            else:
                raise Exception()


# https://www.geeksforgeeks.org/longest-repeating-and-non-overlapping-substring/
def longest_substring(str):
    n = len(str)
    LCSRe = [[0 for x in range(n + 1)]
             for y in range(n + 1)]

    res = "" # To store result
    res_length = 0 # To store length of result

    # building table in bottom-up manner
    index = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):

            # (j-i) > LCSRe[i-1][j-1] to remove
            # overlapping
            if (str[i - 1] == str[j - 1] and
                    LCSRe[i - 1][j - 1] < (j - i)):
                LCSRe[i][j] = LCSRe[i - 1][j - 1] + 1

                # updating maximum length of the
                # substring and updating the finishing
                # index of the suffix
                if (LCSRe[i][j] > res_length and LCSRe[i][j] <= 18):
                    res_length = LCSRe[i][j]
                    index = max(i, index)

            else:
                LCSRe[i][j] = 0

    # If we have non-empty result, then insert
    # all characters from first character to
    # last character of string
    if (res_length > 0):
        for i in range(index - res_length + 1,
                       index + 1):
            res = res + str[i - 1]

    return res


def build_instructions(path):
    steps = 0
    for instruction in path:
        if instruction == "1":
            steps += 1
        else:
            if steps:
                yield str(steps)
                steps = 0
            yield instruction
    if steps:
        yield str(steps)


def build_route(map):
    full_path = ",".join(build_instructions("".join(find_path(map))))
    a = longest_substring(full_path).strip(",")
    full_path = full_path.replace(a, "A")
    remaining_parts = [part.strip(",") for part in full_path.split("A") if part]
    for i, part in enumerate(remaining_parts):
        other_parts = remaining_parts[:i] + remaining_parts[i+1:]
        if any(part in other_part for other_part in other_parts):
            b = part
            break
    else:
        raise Exception("Couldn't figure out a b")
    full_path = full_path.replace(b, "B")
    c = longest_substring(full_path).strip("ABC,")
    full_path = full_path.replace(c, "C")
    return "\n".join([full_path, a, b, c])


def run_robot(program, route):
    input = list(reversed([ord(c) for c in route + "\nn\n"]))
    output = []
    program[0] = 2
    IntcodeVM(program, input.pop, output.append).run()
    if output[-1] > 255:
        return output.pop()
    for c in output:
        sys.stdout.write(chr(c))


with open("input.txt") as input_file:
    INPUT = [int(instruction) for instruction in input_file.read().split(",")]

MAP = build_map(INPUT)
print(f"Part One: {sum(find_intersections(MAP))}")
print(f"Part Two: {run_robot(INPUT, build_route(MAP))}")
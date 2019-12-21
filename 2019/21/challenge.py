#!/usr/bin/env pypy3

from collections import deque
from intcode import IntcodeVM
import sys

with open("input.txt") as input_file:
    SPRINGSCRIPT_VM_CODE = [int(instruction) for instruction in input_file.read().split(",")]


def run_springscript(script, mode):
    input = deque(ord(c) for c in script + f"\n{mode}\n")
    output = deque()
    IntcodeVM(SPRINGSCRIPT_VM_CODE, input.popleft, output.append).run()
    while output:
        c = output.popleft()
        if c > 255:
            return c
        sys.stdout.write(chr(c))

PART_ONE_SPRINGSCRIPT = """
NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
""".strip()
print(f"Part One: {run_springscript(PART_ONE_SPRINGSCRIPT, 'WALK')}")

PART_TWO_SPRINGSCRIPT = """
NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
NOT T T
OR H T
AND T J
""".strip()
print(f"Part Two: {run_springscript(PART_TWO_SPRINGSCRIPT, 'RUN')}")
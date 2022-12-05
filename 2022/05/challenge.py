#!/usr/bin/env python3
import re
import string
from collections import defaultdict, namedtuple

INSTRUCTION_RE = re.compile(r'move (?P<n>\d+) from (?P<origin>\d+) to (?P<dest>\d+)')
Instruction = namedtuple("Instruction", "n origin dest")


def load_input(filename):
    with open(filename) as input_file:
        stacks = defaultdict(list)
        instructions = []
        mode = "stacks"
        for line in input_file.readlines():
            if not line.strip():
                mode = "instructions"
                continue

            if mode == "stacks":
                for col in range(0, len(line), 4):
                    box = line[col+1]
                    if box in string.ascii_uppercase:
                        stacks[str(col // 4 + 1)].insert(0, box)
            else:
                match = INSTRUCTION_RE.match(line)
                instructions.append(Instruction(int(match.group("n")), match.group("origin"), match.group("dest")))

    return stacks, instructions


def part_one(initial_stacks, instructions):
    stacks = {k: list(v) for k, v in initial_stacks.items()}
    for instruction in instructions:
        for _ in range(instruction.n):
            stacks[instruction.dest].append(stacks[instruction.origin].pop())
    return "".join(stacks[k][-1] for k in sorted(stacks.keys()))


def part_two(initial_stacks, instructions):
    stacks = {k: list(v) for k, v in initial_stacks.items()}
    for instruction in instructions:
        moving = stacks[instruction.origin][-instruction.n:]
        stacks[instruction.origin] = stacks[instruction.origin][:-instruction.n]
        stacks[instruction.dest].extend(moving)
    return "".join(stacks[k][-1] for k in sorted(stacks.keys()))


INITIAL_STACKS, INSTRUCTIONS = load_input("input.txt")
print(f"Part One: {part_one(INITIAL_STACKS, INSTRUCTIONS)}")
print(f"Part Two: {part_two(INITIAL_STACKS, INSTRUCTIONS)}")

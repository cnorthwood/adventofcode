#!/usr/bin/env python3

from collections import namedtuple
import re

MEM_RE = re.compile(r'mem\[(?P<address>\d+)] = (?P<value>\d+)')
MASK_RE = re.compile(r'mask = (?P<value>[01X]+)')
MemoryCommand = namedtuple("MemoryCommand", "command address value")
MaskCommand = namedtuple("MaskCommand", "command bitmask")


def parse_bitmask(bitmask):
    return [None if c == "X" else True if c == "1" else False for c in reversed(bitmask)]


def parse_data(lines):
    commands = []
    for line in lines:
        if (match := MEM_RE.match(line)):
            commands.append(MemoryCommand("mem", int(match.group("address")), int(match.group("value"))))
        elif (match := MASK_RE.match(line)):
            commands.append(MaskCommand("mask", parse_bitmask(match.group("value"))))
    return commands


def mask(value, bitmask):
    for i, bit in enumerate(bitmask):
        if bit is None:
            continue
        elif bit:
            value |= 1 << i
        else:
            value &= ~(1 << i)
    return value


def compute_all_possible_values_from_bitmask(bitmask):
    if len(bitmask) == 0:
        yield []
        return
    for possible_value in compute_all_possible_values_from_bitmask(bitmask[1:]):
        if bitmask[0] is True or bitmask[0] is None:
            yield [True] + possible_value
        if bitmask[0] is None:
            yield [False] + possible_value
        if bitmask[0] is False:
            yield [None] + possible_value


def simulate_part_one(commands):
    memory = {}
    bitmask = [None] * 36
    for command in commands:
        if command.command == "mem":
            memory[command.address] = mask(command.value, bitmask)
        elif command.command == "mask":
            bitmask = command.bitmask
    return memory


def simulate_part_two(commands):
    memory = {}
    bitmask = [None] * 36
    for command in commands:
        if command.command == "mem":
            for possible_bitmask in compute_all_possible_values_from_bitmask(bitmask):
                memory[mask(command.address, possible_bitmask)] = command.value
        elif command.command == "mask":
            bitmask = command.bitmask
    return memory


with open("input.txt") as input_file:
    INPUT = parse_data(input_file.readlines())

print(f"Part One: {sum(simulate_part_one(INPUT).values())}")
print(f"Part Two: {sum(simulate_part_two(INPUT).values())}")

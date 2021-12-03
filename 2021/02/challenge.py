#!/usr/bin/env python3
import re
from operator import mul

COMMAND_RE = re.compile(r'(?P<command>forward|down|up) (?P<value>\d+)')


def parse_commands(filename):
    with open(filename) as commands_file:
        for line in commands_file:
            match = COMMAND_RE.match(line)
            if not match:
                raise ValueError(f"Unrecognised line {line}")
            yield match.group("command"), int(match.group("value"))


def track_position(commands):
    x, y = 0, 0
    for command, value in commands:
        if command == "forward":
            x += value
        elif command == "down":
            y += value
        elif command == "up":
            y -= value
        else:
            raise ValueError(f"unknown command {command}")
    return x, y


def track_aim(commands):
    x, y, aim = 0, 0, 0
    for command, value in commands:
        if command == "forward":
            x += value
            y += aim * value
        elif command == "down":
            aim += value
        elif command == "up":
            aim -= value
        else:
            raise ValueError(f"unknown command {command}")
    return x, y


COMMANDS = list(parse_commands("input.txt"))
print(f"Part One: {mul(*track_position(COMMANDS))}")
print(f"Part Two: {mul(*track_aim(COMMANDS))}")

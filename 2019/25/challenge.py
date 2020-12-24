#!/usr/bin/env pypy3

from collections import deque
from itertools import combinations
from intcode import IntcodeVM, Halt
import re
import sys


OPPOSITES = {
    "north": "south",
    "south": "north",
    "west": "east",
    "east": "west",
}


def run_interactive(program):
    def input_reader():
        if input_reader.last_input:
            return input_reader.last_input.popleft()
        for c in input():
            input_reader.last_input.append(ord(c))
        input_reader.last_input.append(ord("\n"))
        return input_reader.last_input.popleft()
    input_reader.last_input = deque()

    def output(output):
        sys.stdout.write(chr(output))

    IntcodeVM(program, input_reader, output).run()


class CommandInput:
    def __init__(self, command):
        if command:
            self._command = deque("\n".join(command))
            self._command.append("\n")
        else:
            self._command = None

    def __call__(self):
        if self._command:
            return ord(self._command.popleft())
        else:
            raise Halt()


class OutputParser:
    ITEM_RE = re.compile(r'You take the [^\n]+\.\s*Command\?')
    PASSWORD_RE = re.compile(r'You should be able to get in by typing (?P<password>\d+) on the keypad')

    def __init__(self):
        self._str = ""

    def __call__(self, val):
        if len(self._str) > 1000:
            raise Halt()
        self._str += chr(val)

    def is_checkpoint(self):
        return "Security Checkpoint" in self._str

    def checkpoint_failed(self):
        return "Alert!" in self._str

    def password(self):
        match = self.PASSWORD_RE.search(self._str)
        if match:
            return match.group("password")

    def pick_up_successfully(self):
        return self.ITEM_RE.search(self._str) is not None

    def directions(self):
        found_directions = False
        for line in self._str.splitlines():
            if line.startswith("Doors here lead:"):
                found_directions = True
                continue
            if not found_directions:
                continue
            if not line.startswith("-"):
                found_directions = False
                continue
            yield line.strip("- ")

    def items(self):
        found_items = False
        for line in self._str.splitlines():
            if line.startswith("Items here:"):
                found_items = True
                continue
            if not found_items:
                continue
            if not line.startswith("-"):
                found_items = False
                continue
            yield line.strip("- ")


def can_pick_up(vm, item):
    # This is annoyingly special-cased
    if item == "giant electromagnet":
        return False
    output_parser = OutputParser()
    vm = vm.clone(CommandInput([f"take {item}"]), output_parser)
    vm.run()
    return output_parser.pick_up_successfully()


def find_items(vm, command, path_so_far):
    output_parser = OutputParser()
    vm = vm.clone(CommandInput([command]), output_parser)
    vm.run()
    if output_parser.is_checkpoint():
        yield path_so_far, ("Checkpoint", next(direction for direction in output_parser.directions() if path_so_far[-1] != OPPOSITES[direction]))
        return
    for item in output_parser.items():
        if can_pick_up(vm, item):
            yield path_so_far, item
    for direction in output_parser.directions():
        if path_so_far and path_so_far[-1] == OPPOSITES[direction]:
            continue
        yield from find_items(vm, direction, path_so_far + [direction])


def collect_all_items(program, item_paths):
    command_list = []
    for path, item in item_paths:
        if item[0] == "Checkpoint":
            continue
        command_list.extend(path)
        command_list.append(f"take {item}")
        command_list.extend(OPPOSITES[step] for step in reversed(path))
    command_list.extend(next(path for path, item in item_paths if item[0] == "Checkpoint"))
    for _, item in item_paths:
        command_list.append(f"drop {item}")
    vm = IntcodeVM(program, CommandInput(command_list), lambda c: None)
    vm.run()
    return vm


def try_combination(vm, items, direction):
    output_parser = OutputParser()
    vm = vm.clone(CommandInput([f"take {item}" for item in items] + [direction]), output_parser)
    vm.run()
    return output_parser.checkpoint_failed(), output_parser.password()


def try_all_object_combos(vm, item_paths):
    direction = next(item[1] for path, item in item_paths if item[0] == "Checkpoint")
    items = [item for path, item in item_paths if item[0] != "Checkpoint"]
    for r in range(len(items)):
        for combination in combinations(items, r):
            failed, password = try_combination(vm, combination, direction)
            if not failed:
                return password


with open("input.txt") as input_file:
    PROGRAM = [int(instruction) for instruction in input_file.read().split(",")]

# run_interactive(PROGRAM)
ITEM_PATHS = list(find_items(IntcodeVM(PROGRAM, None, None), "", []))
AT_CHECKPOINT = collect_all_items(PROGRAM, ITEM_PATHS)
print(f"Part One: {try_all_object_combos(AT_CHECKPOINT, ITEM_PATHS)}")

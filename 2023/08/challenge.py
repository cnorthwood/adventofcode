#!/usr/bin/env python3

from itertools import cycle
from math import lcm
import re


def load_input(filename):
    with open(filename) as input_file:
        lines = input_file.readlines()
        instructions = lines[0].strip()
        nodes = {}
        for line in lines[2:]:
            match = re.match(r'(?P<node>\w+) = \((?P<left>\w+), (?P<right>\w+)\)', line)
            nodes[match.group("node")] = {"L": match.group("left"), "R": match.group("right")}
    return instructions, nodes


def follow_instructions(instructions, nodes, start="AAA", target_func=lambda location: location == "ZZZ"):
    location = start
    for steps, instruction in enumerate(cycle(instructions)):
        if target_func(location):
            return steps
        location = nodes[location][instruction]


def ghost_behaviour(instructions, nodes):
    return lcm(*(follow_instructions(instructions, nodes, start, lambda location: location[-1] == "Z") for start in nodes.keys() if start[-1] == "A"))


INSTRUCTIONS, NODES = load_input("input.txt")
print(f"Part One: {follow_instructions(INSTRUCTIONS, NODES)}")
print(f"Part Two: {ghost_behaviour(INSTRUCTIONS, NODES)}")

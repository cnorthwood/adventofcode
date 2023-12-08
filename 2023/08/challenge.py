#!/usr/bin/env python3

from itertools import cycle
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


def follow_instructions(instructions, nodes, target="ZZZ"):
    location = "AAA"
    for steps, instruction in enumerate(cycle(instructions)):
        if location == target:
            return steps
        location = nodes[location][instruction]


def ghost_behaviour(instructions, nodes):
    locations = [location for location in nodes.keys() if location[-1] == "A"]
    for steps, instruction in enumerate(cycle(instructions)):
        if all(location[-1] == "Z" for location in locations):
            return steps
        locations = [nodes[location][instruction] for location in locations]


INSTRUCTIONS, NODES = load_input("input.txt")
print(f"Part One: {follow_instructions(INSTRUCTIONS, NODES)}")
# print(f"Part Two: {ghost_behaviour(INSTRUCTIONS, NODES)}")

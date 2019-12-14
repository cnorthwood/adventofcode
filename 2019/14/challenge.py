#!/usr/bin/env pypy3

from collections import defaultdict, namedtuple
from math import ceil

Instruction = namedtuple("Instruction", "amount inputs")
Input = namedtuple("Input", "amount compound")


def parse_lines(lines):
    instructions = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        inputs, output = line.split(" => ")
        output_amount, output_compound = output.split(" ")
        instructions[output_compound] = Instruction(int(output_amount), [])
        for input in inputs.split(", "):
            input_amount, input_compound = input.split(" ")
            instructions[output_compound].inputs.append(Input(int(input_amount), input_compound))
    return instructions


def ore_required(instructions, available_ingredients, target="FUEL", target_amount=1):
    if target == "ORE":
        return target_amount, target_amount
    ore_used = 0
    instruction = instructions[target]
    num_reactions = ceil(target_amount / instruction.amount)
    for input in instruction.inputs:
        ore_used_for_input, amount_made = ore_required(
            instructions,
            available_ingredients,
            input.compound,
            (input.amount * num_reactions) - available_ingredients[input.compound]
        )
        ore_used += ore_used_for_input
        available_ingredients[input.compound] += amount_made - input.amount * num_reactions
    return ore_used, instruction.amount * num_reactions


def fuel_for_ore(instructions, ore_per_fuel, max_ore=1000000000000):
    lower, higher = max_ore // ore_per_fuel, 2 * (max_ore // ore_per_fuel)
    while lower != higher - 1:
        test_fuel = lower + (higher - lower) // 2
        ore = ore_required(instructions, defaultdict(int), target_amount=test_fuel)[0]
        if ore > max_ore:
            higher = test_fuel
        elif ore < max_ore:
            lower = test_fuel
    return lower


with open("input.txt") as input_file:
    INPUT = parse_lines(input_file.readlines())

ore_per_fuel = ore_required(INPUT, defaultdict(int))[0]
print(f"Part One: {ore_per_fuel}")
print(f"Part Two: {fuel_for_ore(INPUT, ore_per_fuel)}")

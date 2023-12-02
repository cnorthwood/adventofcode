#!/usr/bin/env python3

from collections import defaultdict
from math import prod


def parse_draws(bag):
    contents = {}
    for pair in bag.split(", "):
        num, colour = pair.split()
        contents[colour] = int(num)
    return contents


def parse_game(line):
    game_part, draws_part = line.split(": ")
    game_id = int(game_part.split()[-1])
    return game_id, [parse_draws(draw) for draw in draws_part.split("; ")]


def load_input(filename):
    with open(filename) as input_file:
        return dict(parse_game(line.strip()) for line in input_file.readlines())


def is_possible_draw(draw):
    return draw.get("red", 0) <= 12 and draw.get("green", 0) <= 13 and draw.get("blue", 0) <= 14


def minimal_bag(draws):
    draws_by_colour = defaultdict(list)
    for draw in draws:
        for colour, num in draw.items():
            draws_by_colour[colour].append(num)
    return {colour: max(colour_draws) for colour, colour_draws in draws_by_colour.items()}


GAMES = load_input("input.txt")
print(f"Part One: {sum(game_id for game_id, draws in GAMES.items() if all(is_possible_draw(draw) for draw in draws))}")
print(f"Part Two: {sum(prod(minimal_bag(draws).values()) for draws in GAMES.values())}")
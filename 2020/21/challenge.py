#!/usr/bin/env python3

from collections import defaultdict
import re
from itertools import chain

INPUT_RE = re.compile(r'^(?P<ingredients>.+) \(contains (?P<allergens>.+)\)$')


def parse_input(input_file):
    for line in input_file.readlines():
        match = INPUT_RE.match(line.strip())
        yield frozenset(match.group("ingredients").split()), frozenset(match.group("allergens").split(", "))


def sieve_allergens(meals):
    all_ingredients = frozenset(chain.from_iterable(ingredients for ingredients, _ in meals))
    possible_containing_ingredients = {allergen: set(all_ingredients) for allergen in chain.from_iterable(allergens for _, allergens in meals)}
    for ingredients, allergens in meals:
        for allergen in allergens:
            possible_containing_ingredients[allergen] &= ingredients
    return all_ingredients - frozenset(chain.from_iterable(possible_containing_ingredients.values())), possible_containing_ingredients


def find_unique_ingredients(possible_containing_ingredients):
    while not all(len(possibilities) == 1 for possibilities in possible_containing_ingredients.values()):
        for allergen, possibilities in possible_containing_ingredients.items():
            if len(possibilities) == 1:
                for other_allergen in possible_containing_ingredients.keys():
                    if allergen == other_allergen:
                        continue
                    possible_containing_ingredients[other_allergen] -= possibilities
    return possible_containing_ingredients


with open("input.txt") as input_file:
    INPUT = list(parse_input(input_file))
ALLERGEN_FREE_INGREDIENTS, ALLERGEN_CONTAINING_INGREDIENTS = sieve_allergens(INPUT)
print(f"Part One: {sum(len(ALLERGEN_FREE_INGREDIENTS & meal) for meal, _ in INPUT)}")
print(
    "Part Two:",
    ",".join(
        ingredient.pop() for _, ingredient in sorted(
            find_unique_ingredients(ALLERGEN_CONTAINING_INGREDIENTS).items(),
            key=lambda item: item[0]
        )
    )
)

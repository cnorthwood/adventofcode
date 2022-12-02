#!/usr/bin/env python3

from enum import Enum

Shape = Enum("Shape", ["PAPER", "ROCK", "SCISSORS"])

ENCRYPTED_MAPPING = {
    "A": Shape.ROCK,
    "B": Shape.PAPER,
    "C": Shape.SCISSORS,
    "X": Shape.ROCK,
    "Y": Shape.PAPER,
    "Z": Shape.SCISSORS,
}

LOSS = 0
DRAW = 3
WIN = 6

SCORES = {
    Shape.ROCK: {
        "value": 1,
        Shape.ROCK: DRAW,
        Shape.SCISSORS: WIN,
        Shape.PAPER: LOSS,
    },
    Shape.PAPER: {
        "value": 2,
        Shape.ROCK: WIN,
        Shape.SCISSORS: LOSS,
        Shape.PAPER: DRAW,
    },
    Shape.SCISSORS: {
        "value": 3,
        Shape.ROCK: LOSS,
        Shape.SCISSORS: DRAW,
        Shape.PAPER: WIN,
    },
}


def part_one_score(their_hand, my_hand):
    return SCORES[ENCRYPTED_MAPPING[my_hand]]["value"] + SCORES[ENCRYPTED_MAPPING[my_hand]][ENCRYPTED_MAPPING[their_hand]]


ENCRYPTED_PART_TWO = {
    "X": LOSS,
    "Y": DRAW,
    "Z": WIN,
}


def desired_shape(their_shape, desired_outcome):
    for shape in Shape:
        if SCORES[shape][their_shape] == desired_outcome:
            return shape


def part_two_score(their_hand, desired_outcome):
    desired_outcome = ENCRYPTED_PART_TWO[desired_outcome]
    my_shape = desired_shape(ENCRYPTED_MAPPING[their_hand], desired_outcome)
    return SCORES[my_shape]["value"] + desired_outcome


with open("input.txt") as input_file:
    INPUT = [tuple(line.strip().split()) for line in input_file.readlines()]

print(f"Part One: {sum(part_one_score(*hand) for hand in INPUT)}")
print(f"Part Two: {sum(part_two_score(*hand) for hand in INPUT)}")

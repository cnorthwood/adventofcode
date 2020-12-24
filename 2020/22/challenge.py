#!/usr/bin/env pypy3

from collections import deque


def parse_input(input_file):
    decks = []
    for line in input_file.readlines():
        if line.startswith("Player"):
            decks.append(deque())
        elif line.strip().isdigit():
            decks[-1].append(int(line.strip()))
    return decks


def copy_decks(decks):
    return [deque(deck) for deck in decks]


def part_one_round(left, right):
    left_card = left.popleft()
    right_card = right.popleft()
    return left_card > right_card, left_card, right_card


def part_two_round(left, right):
    left_card = left.popleft()
    right_card = right.popleft()
    if len(left) >= left_card and len(right) >= right_card:
        subgame_decks = simulate(copy_decks([list(left)[:left_card], list(right)[:right_card]]), part_two_round)
        return len(subgame_decks[0]) > len(subgame_decks[1]), left_card, right_card
    return left_card > right_card, left_card, right_card


def simulate(decks, play_round):
    seen = set()
    while all(len(deck) > 0 for deck in decks):
        left, right = decks
        this_game = (tuple(left), tuple(right))
        if this_game in seen:
            return left, []
        seen.add(this_game)
        left_wins, left_card, right_card = play_round(left, right)
        if left_wins:
            decks[0].append(left_card)
            decks[0].append(right_card)
        else:
            decks[1].append(right_card)
            decks[1].append(left_card)
    return decks


def score(deck):
    return sum((i+1) * card for i, card in enumerate(reversed(deck)))


SEEN = set()
with open("input.txt") as input_file:
    INPUT = parse_input(input_file)

print(f"Part One: {max(score(deck) for deck in simulate(copy_decks(INPUT), part_one_round))}")
print(f"Part Two: {max(score(deck) for deck in simulate(copy_decks(INPUT), part_two_round))}")

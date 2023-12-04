#!/usr/bin/env python3

def parse_input(filename):
    with open(filename) as input_file:
        for line in input_file.readlines():
            winning_numbers, card_numbers = line.split(":")[1].split("|")
            yield {int(n) for n in winning_numbers.split()}, {int(n) for n in card_numbers.split()}


def num_matches(card):
    winning_numbers, card_numbers = card
    return len(winning_numbers & card_numbers)


def score(card):
    n = num_matches(card)
    if n == 0:
        return 0
    return 2**(n-1)


def part2_score(cards):
    stack_size = [1] * len(cards)
    for i, card in enumerate(cards):
        for j in range(i + 1, i + num_matches(card) + 1):
            stack_size[j] += stack_size[i]
    return sum(stack_size)


INPUT = list(parse_input("input.txt"))
print(f"Part One: {sum(score(card) for card in INPUT)}")
print(f"Part Two: {part2_score(INPUT)}")

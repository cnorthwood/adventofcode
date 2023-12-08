#!/usr/bin/env python3

from collections import Counter

CARD_WEIGHTS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def hand_rank(hand):
    c = sorted(Counter(hand).values())
    if c == [5]:  # five of a kind
        return 6
    elif c == [1, 4]:  # four of a kind
        return 5
    elif c == [2, 3]:  # full house
        return 4
    elif c == [1, 1, 3]:  # three of a kind
        return 3
    elif c == [1, 2, 2]:  # two pair
        return 2
    elif c == [1, 1, 1, 2]:  # pair
        return 1
    else:  # high card
        return 0


def hand_score(hand):
    return tuple([hand_rank(hand), *map(CARD_WEIGHTS.get, hand)])


def load_input(filename):
    hand_bids = {}
    with open(filename) as input_file:
        for line in input_file.readlines():
            hand, bid = line.split()
            hand_bids[hand] = int(bid)
    return hand_bids


def jokered_hand_rank(hand):
    other_cards = set(CARD_WEIGHTS.keys() - {"J"})
    return max(hand_rank(hand.replace("J", other_card)) for other_card in other_cards)


def jokered_hand_score(hand):
    return tuple([jokered_hand_rank(hand), *map(CARD_WEIGHTS.get, hand)])


def part_one(hand_bids):
    ranked_hands = sorted(hand_bids.keys(), key=hand_score)
    return sum(hand_bids[hand] * (i + 1) for i, hand in enumerate(ranked_hands))


def part_two(hand_bids):
    ranked_hands = sorted(hand_bids.keys(), key=jokered_hand_score)
    return sum(hand_bids[hand] * (i + 1) for i, hand in enumerate(ranked_hands))


INPUT = load_input("input.txt")
print(f"Part One: {part_one(INPUT)}")
CARD_WEIGHTS["J"] = 1
print(f"Part Two: {part_two(INPUT)}")

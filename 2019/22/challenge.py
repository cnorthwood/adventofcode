#!/usr/bin/env pypy3

DECK_SIZE = 119315717514047
SHUFFLES = 101741582076661


def deal_into_new_stack(cards):
    return list(reversed(cards))


def deal_into_new_stack_rev(a, b):
    return -a % DECK_SIZE, (DECK_SIZE - 1 - b) % DECK_SIZE


def cut_n(cards, n):
    return cards[n:] + cards[:n]


def cut_n_rev(n, a, b):
    return a, (b - n) % DECK_SIZE


def deal_with_increment_n(cards, n):
    shuffled_cards = [None] * len(cards)
    for i, card in enumerate(cards):
        shuffled_cards[(i * n) % len(cards)] = card
    return shuffled_cards


def deal_with_increment_n_rev(n, a, b):
    return a * n % DECK_SIZE, b * n % DECK_SIZE


def shuffle(instructions, deck_size=10007):
    cards = list(range(deck_size))
    for instruction in instructions:
        if instruction.startswith("deal into new stack"):
            cards = deal_into_new_stack(cards)
        elif instruction.startswith("cut"):
            n = int(instruction.split()[-1])
            cards = cut_n(cards, n)
        elif instruction.startswith("deal with increment"):
            n = int(instruction.split()[-1])
            cards = deal_with_increment_n(cards, n)
        else:
            raise Exception(f"Unknown instruction: {instruction}")
    return cards


def part_two(instructions, position=2020):
    # I don't really understand the maths here
    a = 1
    b = 0
    for instruction in instructions:
        if instruction.startswith("deal into new stack"):
            a, b = deal_into_new_stack_rev(a, b)
        elif instruction.startswith("cut"):
            n = int(instruction.split()[-1])
            a, b = cut_n_rev(n, a, b)
        elif instruction.startswith("deal with increment"):
            n = int(instruction.split()[-1])
            a, b = deal_with_increment_n_rev(n, a, b)
        else:
            raise Exception(f"Unknown instruction: {instruction}")
    r = (b * pow(1 - a, DECK_SIZE - 2, DECK_SIZE)) % DECK_SIZE
    return ((position - r) * pow(a, SHUFFLES * (DECK_SIZE - 2), DECK_SIZE) + r) % DECK_SIZE


# assert(" ".join(deal_into_new_stack("0 1 2 3 4 5 6 7 8 9".split())) == "9 8 7 6 5 4 3 2 1 0")
# assert(" ".join(cut_n("0 1 2 3 4 5 6 7 8 9".split(), 3)) == "3 4 5 6 7 8 9 0 1 2")
# assert(" ".join(cut_n("0 1 2 3 4 5 6 7 8 9".split(), -4)) == "6 7 8 9 0 1 2 3 4 5")
# assert(" ".join(deal_with_increment_n("0 1 2 3 4 5 6 7 8 9".split(), 3)) == "0 7 4 1 8 5 2 9 6 3")


with open("input.txt") as input_file:
    INPUT = input_file.read().strip().splitlines(keepends=False)

print(f"Part One: {shuffle(INPUT).index(2019)}")
print(f"Part Two: {part_two(INPUT)}")

#!/usr/bin/env pypy3

from itertools import chain
import re
import string

TEST = 'dabAcCaCBAcCcaDA'

pairs = list(
    map(lambda p: ''.join(p), chain(
        zip(string.ascii_lowercase, string.ascii_uppercase),
        zip(string.ascii_uppercase, string.ascii_lowercase)
    ))
)

PAIRS_RE = re.compile('({})'.format('|'.join(pairs)))


def annihilate(polymer):
    polymer, subs_made = PAIRS_RE.subn('', polymer)
    if subs_made == 0:
        return len(polymer)
    else:
        return annihilate(polymer)


assert(annihilate(TEST) == 10)

with open('input.txt') as input_file:
    INPUT = input_file.read().strip()

print("Part One: {}".format(annihilate(INPUT)))


def eliminate_problem(polymer, letter):
    polymer = re.sub(letter, '', polymer, flags=re.I)
    return annihilate(polymer)


def part_two(polymer):
    return min(eliminate_problem(polymer, letter) for letter in string.ascii_lowercase)


assert(part_two(TEST) == 4)
print("Part Two: {}".format(part_two(INPUT)))

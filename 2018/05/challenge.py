#!/usr/bin/env pypy3

from itertools import chain
import re
import string
import sys

sys.setrecursionlimit(10000)

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
        return polymer
    else:
        return annihilate(polymer)


TEST_POLYMER = annihilate(TEST)
assert(len(TEST_POLYMER) == 10)

with open('input.txt') as input_file:
    INPUT = input_file.read().strip()

POLYMER = annihilate(INPUT)
print("Part One: {}".format(len(POLYMER)))


def eliminate_problem(polymer, letter):
    polymer = re.sub(letter, '', polymer, flags=re.I)
    return len(annihilate(polymer))


def part_two(polymer):
    return min(eliminate_problem(polymer, letter) for letter in string.ascii_lowercase)


assert(part_two(TEST_POLYMER) == 4)
print("Part Two: {}".format(part_two(POLYMER)))

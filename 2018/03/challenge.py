#!/usr/bin/env pypy3

from collections import Counter, namedtuple
import re

TEST = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""

LINE_RE = re.compile(r'#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)')

Claim = namedtuple('Claim', 'id coverage')


def covered(origin_x, origin_y, w, h):
    for x in range(origin_x, origin_x + w):
        for y in range(origin_y, origin_y + h):
            yield x, y


def parse_line(line):
    match = LINE_RE.match(line)
    return Claim(int(match.group('id')),
                 list(covered(int(match.group('x')),
                              int(match.group('y')),
                              int(match.group('w')),
                              int(match.group('h')))))


# test_claims = list(map(parse_line, TEST.strip().splitlines()))
with open('input.txt') as input_file:
    CLAIMS = list(map(parse_line, input_file.read().strip().splitlines()))


def build_cloth_claims(claims):
    squares = Counter()
    for claim in claims:
        for x, y in claim.coverage:
            squares[x, y] += 1
    return squares


def overlapping_squares(squares):
    return len([n for n in squares.values() if n > 1])


# test_cloth_claims = build_cloth_claims(test_claims)
CLOTH_CLAIMS = build_cloth_claims(CLAIMS)

# assert(overlapping_squares(test_cloth_claims) == 4)
print("Part One: {}".format(overlapping_squares(CLOTH_CLAIMS)))


def find_exact_match(claims, cloth_claims):
    for claim in claims:
        if all(cloth_claims[x, y] == 1 for x, y in claim.coverage):
            return claim.id


# assert(find_exact_match(test_claims, test_cloth_claims) == 3)
print("Part Two: {}".format(find_exact_match(CLAIMS, CLOTH_CLAIMS)))

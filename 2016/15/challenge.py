from collections import namedtuple
from itertools import count
import re

INPUT_RE = re.compile(r'Disc #(?P<disc_id>\d) has (?P<positions>\d+) positions; at time=0, it is at position (?P<initial>\d+).')

DISCS = []
Disc = namedtuple('Disc', 'initial positions')


def is_open(disc, t):
    return (disc.initial + t) % disc.positions == 0

with open('input.txt') as input:
    for line in input:
        disc_info = INPUT_RE.match(line).groupdict()
        DISCS.append(Disc(int(disc_info['initial']), int(disc_info['positions'])))

for t in count():
    if all(is_open(disc, t + i + 1) for i, disc in enumerate(DISCS)):
        print "Part One:", t
        break

DISCS.append(Disc(0, 11))

for t in count():
    if all(is_open(disc, t + i + 1) for i, disc in enumerate(DISCS)):
        print "Part Two:", t
        break

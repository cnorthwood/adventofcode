#!/usr/bin/env pypy3

import re
import sys

INPUT_RE = re.compile(r'(?P<d1>[xy])=(?P<v1>\d+), (?P<d2>[xy])=(?P<v2s>\d+)..(?P<v2e>\d+)')


def load_clay(filename):
    with open(filename) as input_file:
        lines = input_file.read().strip().splitlines()
    for line in lines:
        match = INPUT_RE.match(line)
        if match.group('d1') == 'x' and match.group('d2') == 'y':
            x = int(match.group('v1'))
            for y in range(int(match.group('v2s')), int(match.group('v2e')) + 1):
                yield x, y
        elif match.group('d1') == 'y' and match.group('d2') == 'x':
            y = int(match.group('v1'))
            for x in range(int(match.group('v2s')), int(match.group('v2e')) + 1):
                yield x, y
        else:
            raise ValueError()


TEST = set(load_clay('test.txt'))
BLOCKS = set(load_clay('input.txt'))


def visualise(blocks, edges, clay):
    min_x = min(x for x, y in blocks | set(edges) | clay)
    min_y = min(y for x, y in blocks | set(edges) | clay)
    max_x = max(x for x, y in blocks | set(edges) | clay)
    max_y = max(y for x, y in blocks | set(edges) | clay)
    sys.stdout.write('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    for y in range(min_y, max_y  + 1):
        for x in range(min_x, max_x  + 1):
            if (x, y) in clay:
                sys.stdout.write('█')
            elif (x, y) in blocks:
                sys.stdout.write('W')
            elif (x, y) in edges:
                sys.stdout.write('~')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')


def simulate(clay):
    blocks = set()
    edges = [(500, 0)]
    max_y = max(y for x, y in clay)
    while edges:
        visualise(blocks, edges, clay)
        edges = sorted(edges, key=lambda pos: pos[1], reverse=True)
        x, y = edges[0]
        if (x, y + 1) not in clay and (x, y + 1) not in blocks:
            edges.append((x, y + 1))
            if y + 1 <= max_y:
                edges.append((x, y + 1))

    return sum(1 for x, y in (blocks | edges) if y >= min(y for x, y in clay))


assert(simulate(TEST) == 57)

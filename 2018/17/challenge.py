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


def visualise(blocks, edges, clay, stdout=False):
    min_x = min(x for x, y in blocks | edges | clay)
    min_y = min(y for x, y in blocks | edges | clay)
    max_x = max(x for x, y in blocks | edges | clay)
    max_y = max(y for x, y in blocks | edges | clay)
    if stdout:
        output = sys.stdout
    else:
        output = open('debug.txt', 'w')
    for y in range(min_y, max_y  + 1):
        for x in range(min_x, max_x  + 1):
            if (x, y) in clay:
                output.write('█')
            elif (x, y) in blocks:
                output.write('W')
            elif (x, y) in edges:
                output.write('~')
            else:
                output.write(' ')
        output.write('\n')
    if not stdout:
        output.close()


def simulate(clay):
    blocks = set()
    edges = {(500, 0)}
    max_y = max(y for x, y in clay)
    touched_edge = False
    while edges:
        # if len(edges) % 100 == 0:
        #     visualise(blocks, edges, clay)
        x, y = max(edges, key=lambda pos: pos[1])
        if (x, y + 1) not in clay | blocks | edges:
            if y + 1 <= max_y:
                edges.add((x, y + 1))
            else:
                touched_edge = True
                for up_y in range(y, 0, step=-1):
                    if (x, up_y) in edges:
                        blocks.add((x, up_y))
                        edges.remove((x, up_y))
                    else:
                        break
        elif (touched_edge and (x, y + 1) in clay) or (not touched_edge and (x, y + 1) in clay | blocks):
            if (x - 1, y) not in clay | blocks | edges:
                edges.add((x - 1, y))
            if (x + 1, y) not in clay | blocks | edges:
                edges.add((x + 1, y))
            blocks.add((x, y))
            edges.remove((x, y))
        elif touched_edge and (x, y + 1) in blocks:
            blocks.add((x, y))
            edges.remove((x, y))

    return sum(1 for x, y in blocks if y >= min(y for x, y in clay))


assert(simulate(TEST) == 57)
print("Part One: {}".format(simulate(BLOCKS)))

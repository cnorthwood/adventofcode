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


def visualise(flowing_water, resting_water, clay, stdout=False):
    min_x = min(x for x, y in flowing_water | resting_water | clay)
    min_y = min(y for x, y in flowing_water | resting_water | clay)
    max_x = max(x for x, y in flowing_water | resting_water | clay)
    max_y = max(y for x, y in flowing_water | resting_water | clay)
    if stdout:
        output = sys.stdout
        output.write('\n\n~~~~~~~~~~~~~~~\n\n')
    else:
        output = open('debug.txt', 'w')
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in clay:
                output.write('█')
            elif (x, y) in resting_water:
                output.write('W')
            elif (x, y) in flowing_water:
                output.write('~')
            else:
                output.write(' ')
        output.write('\n')
    if not stdout:
        output.close()


def is_contained(x, y, min_x, max_x, clay, water):
    for left_x in range(x, min_x - 1, step=-1):
        if (left_x, y + 1) not in clay and (left_x, y + 1) not in water:
            return False
        if (left_x, y) in clay:
            for right_x in range(x, max_x + 1):
                if (right_x, y + 1) not in clay and (right_x, y + 1) not in water:
                    return False
                if (right_x, y) in clay:
                    return True


def simulate(clay):
    flowing_water = {(500, 0)}
    resting_water = set()
    min_x = min(x for x, y in clay)
    max_x = max(x for x, y in clay)
    min_y = min(y for x, y in clay)
    max_y = max(y for x, y in clay)
    last_size = (0, 0)
    while last_size != (len(flowing_water), len(resting_water)):
        last_size = (len(flowing_water), len(resting_water))
        for x, y in sorted(flowing_water, key=lambda pos: pos[1]):
            if (x, y + 1) not in clay and (x, y + 1) not in resting_water:
                if y <= max_y:
                    flowing_water.add((x, y + 1))
            else:
                if is_contained(x, y, min_x, max_x, clay, resting_water):
                    flowing_water.remove((x, y))
                    resting_water.add((x, y))
                if (x - 1, y) not in clay and (x - 1, y) not in resting_water:
                    flowing_water.add((x - 1, y))
                if (x + 1, y) not in clay and (x + 1, y) not in resting_water:
                    flowing_water.add((x + 1, y))
    return len(list(filter(lambda pos: min_y <= pos[1] <= max_y, flowing_water | resting_water))), len(resting_water)


# assert(simulate(TEST) == (57, 29))
part_one, part_two = simulate(BLOCKS)
print("Part One: {}".format(part_one))
print("Part Two: {}".format(part_two))

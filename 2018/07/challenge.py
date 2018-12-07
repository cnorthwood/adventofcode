#!/usr/bin/env pypy3

import re
from collections import defaultdict
from itertools import chain

INPUT_RE = re.compile(r'Step (?P<prereq>.) must be finished before step (?P<step>.) can begin')


def load_input(filename):
    steps = defaultdict(set)
    with open(filename) as input_file:
        for line in input_file.read().strip().splitlines():
            match = INPUT_RE.match(line)
            steps[match.group('step')].add(match.group('prereq'))
    for dep in chain(*steps.values()):
        steps[dep] |= set()
    return steps


def order(deps):
    deps = {step: set(prereqs) for step, prereqs in deps.items()}
    while deps:
        next_step = sorted(filter(lambda step: len(deps[step]) == 0, deps.keys()))[0]
        yield next_step
        del deps[next_step]
        for step in deps.keys():
            deps[step] -= {next_step}


TEST = load_input('test.txt')
INPUT = load_input('input.txt')


assert(''.join(order(TEST)) == 'CABDFE')
print("Part One: {}".format(''.join(order(INPUT))))

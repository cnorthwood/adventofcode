#!/usr/bin/env pypy3

from collections import defaultdict
from itertools import count
import re

INPUT_RE = re.compile(r'Step (?P<prereq>.) must be finished before step (?P<step>.) can begin')


def load_input(filename):
    steps = defaultdict(set)
    with open(filename) as input_file:
        for line in input_file.read().strip().splitlines():
            match = INPUT_RE.match(line)
            steps[match.group('step')].add(match.group('prereq'))
            steps[match.group('prereq')] |= set()
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


def multi_order(deps, num_workers, step_time=lambda s: ord(s) - 4):
    deps = {step: set(prereqs) for step, prereqs in deps.items()}
    workers = [None] * num_workers
    for t in count():
        for i, worker in enumerate(workers):
            if worker is not None:
                working_on, end_time = worker
                if end_time == t:
                    del deps[working_on]
                    for step in deps.keys():
                        deps[step] -= {working_on}
                    worker = None

            if worker is None:
                next_steps = sorted(
                    filter(
                        lambda step: len(deps[step]) == 0
                                     and step not in {w[0] for w in workers if w is not None},
                        deps.keys()
                    ),
                    reverse=True
                )
                if next_steps:
                    workers[i] = (next_steps[0], t + step_time(next_steps[0]))
                else:
                    workers[i] = None
        if not deps:
            return t


assert(multi_order(TEST, 2, step_time=lambda s: ord(s) - 64) == 15)
print("Part Two: {}".format(multi_order(INPUT, 5)))


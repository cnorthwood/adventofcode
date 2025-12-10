#!/usr/bin/env pypy3

from collections import deque
from functools import cache
import re


MACHINE_LINE_RE = re.compile(r'\[(?P<desired_indicators>[\.\#]+)\] (?P<buttons>(\((\d+,)*\d+\) )+)\{(?P<joltages>(\d+,)*\d+)\}')

def load_input(filename):
    with open(filename) as input_file:
        for line in input_file.readlines():
            match = MACHINE_LINE_RE.match(line.strip())
            if not match:
                raise ValueError(line)

            desired_indicators = tuple([{".": False, "#": True}[c] for c in match.group("desired_indicators")])
            buttons = {frozenset({int(d) for d in button_actions.strip("()").split(",")}) for button_actions in match.group("buttons").split()}
            joltages = [int(d) for d in match.group("joltages").split(",")]

            yield desired_indicators, buttons, joltages


@cache
def toggle(indicators, button):
    return tuple(not state if i in button else state for i, state in enumerate(indicators))


def min_pushes(desired_indicators, buttons):
    queue = deque([(0, tuple([False] * len(desired_indicators)))])

    while nextq := queue.popleft():
        n, current_state = nextq
        n += 1

        for button in buttons:
            next_state = toggle(current_state, button)
            if all(not on for on in next_state):
                # we've ended up looping
                continue
            if next_state == desired_indicators:
                return n
            queue.append((n, next_state))


INPUT = list(load_input("input.txt"))
print(f"Part One: {sum(min_pushes(desired_indicators, buttons) for desired_indicators, buttons, _ in INPUT)}")

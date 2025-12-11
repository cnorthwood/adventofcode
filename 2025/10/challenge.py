#!/usr/bin/env python3

from collections import deque
from functools import cache
import numpy as np
import re
from scipy.optimize import milp, LinearConstraint, Bounds


MACHINE_LINE_RE = re.compile(r'\[(?P<desired_indicators>[\.\#]+)\] (?P<buttons>(\((\d+,)*\d+\) )+)\{(?P<joltages>(\d+,)*\d+)\}')

def load_input(filename):
    with open(filename) as input_file:
        for line in input_file.readlines():
            match = MACHINE_LINE_RE.match(line.strip())
            if not match:
                raise ValueError(line)

            desired_indicators = tuple([{".": False, "#": True}[c] for c in match.group("desired_indicators")])
            buttons = {frozenset({int(d) for d in button_actions.strip("()").split(",")}) for button_actions in match.group("buttons").split()}
            joltages = tuple([int(d) for d in match.group("joltages").split(",")])

            yield desired_indicators, buttons, joltages


@cache
def toggle(indicators, button):
    return tuple(not state if i in button else state for i, state in enumerate(indicators))


def min_indicator_pushes(desired_indicators, buttons):
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


def joltage_push(current_state, button):
    return tuple(current_value + (1 if i in button else 0) for i, current_value in enumerate(current_state))


def min_joltage_pushes(desired_joltage, buttons):
    # Build matrix: A[j][i] = 1 if button i affects output j
    effects_matrix = np.zeros((len(desired_joltage), len(buttons)))
    for i, button in enumerate(buttons):
        for j in button:
            effects_matrix[j, i] = 1

    target = np.array(desired_joltage)

    # Minimize sum(x) subject to Ax = b, x >= 0, x integer
    c = np.ones(len(buttons))  # minimize sum of x
    constraints = LinearConstraint(effects_matrix, target, target)  # Ax = b
    bounds = Bounds(lb=0, ub=np.inf)
    integrality = np.ones(len(buttons))

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    return int(round(result.fun))


INPUT = list(load_input("input.txt"))
print(f"Part One: {sum(min_indicator_pushes(desired_indicators, buttons) for desired_indicators, buttons, _ in INPUT)}")
print(f"Part Two: {sum(min_joltage_pushes(desired_joltage, buttons) for _, buttons, desired_joltage in INPUT)}")

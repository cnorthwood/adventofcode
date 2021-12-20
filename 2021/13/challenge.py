#!/usr/bin/env python3

import re

FOLD_RE = re.compile("fold along (?P<axis>[xy])=(?P<val>\d+)")


def load_input(filename):
    dots = set()
    folds = []
    with open(filename) as input_file:
        for line in input_file:
            if line.startswith("fold along"):
                match = FOLD_RE.match(line)
                folds.append((match.group("axis"), int(match.group("val"))))
            elif line.strip():
                x, y = line.strip().split(",")
                dots.add((int(x), int(y)))
    return frozenset(dots), folds


def fold(start, axis, val):
    return frozenset(
        (
            x if axis == "y" else min(x, val) - max(0, x - val),
            y if axis == "x" else min(y, val) - max(0, y - val)
        )
        for x, y in start
    )


def visualise(sheet):
    max_x = max(x for x, y in sheet)
    max_y = max(y for x, y in sheet)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print("█" if (x, y) in sheet else " ", end ="")
        print()


sheet, folds = load_input("input.txt")
for i, (axis, val) in enumerate(folds):
    sheet = fold(sheet, axis, val)
    if i == 0:
        print(f"Part One: {len(sheet)}")
visualise(sheet)

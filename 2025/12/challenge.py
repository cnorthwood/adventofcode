#!/usr/bin/env python3

from collections import namedtuple


PresentArea = namedtuple("PresentArea", "w h n_presents")

def load_input(filename):
    shapes = []
    areas = []
    this_shape = None
    with open(filename) as input_file:
        for line in input_file.readlines():
            if line.strip() == "" and this_shape is not None:
                shapes.append(this_shape)
                this_shape = None
            elif "x" in line:
                dimensions, n_presents = line.strip().split(": ")
                w, h = dimensions.split("x")
                areas.append(PresentArea(w=int(w), h=int(h), n_presents=list(map(int, n_presents.split()))))
            elif ":" in line:
                shape_y = -1
                this_shape = set()
            else:
                shape_y += 1
                this_shape |= {(x, shape_y) for x, c in enumerate(line) if c == "#"}
    return shapes, areas


SHAPES, AREAS = load_input("input.txt")


# lol I did not expect this very naive approach to work
def can_fit(area):
    total_size = area.w * area.h
    min_space_required = sum(n * len(SHAPES[i]) for i, n in enumerate(area.n_presents))
    return total_size >= min_space_required


print(f"Part One: {sum(1 for area in AREAS if can_fit(area))}")

#!/usr/bin/env pypy3

from collections import defaultdict
from math import inf


def load_input(filename):
    with open(filename) as input_file:
        depth_line, target_line = input_file.read().strip().splitlines()
        depth = int(depth_line.split(':')[1])
        target = tuple(map(int, target_line.split(':')[1].strip().split(',')))
    return depth, target


class Cave:

    ROCKY = 0
    WET = 1
    NARROW = 2

    NEITHER = 0b001
    TORCH = 0b010
    CLIMBING = 0b100

    def __init__(self, depth, target):
        self._depth = depth
        self.target = target
        self._geologic = {}
        self._erosion = {}

    def geologic(self, x, y):
        if (x, y) not in self._geologic:
            if (x, y) == (0, 0):
                self._geologic[x, y] = 0
            elif (x, y) == self.target:
                self._geologic[x, y] = 0
            elif x == 0:
                self._geologic[x, y] = y * 48271
            elif y == 0:
                self._geologic[x, y] = x * 16807
            else:
                self._geologic[x, y] = self.erosion(x - 1, y) * self.erosion(x, y - 1)
        return self._geologic[x, y]

    def erosion(self, x, y):
        if (x, y) not in self._erosion:
            self._erosion[x, y] = (self.geologic(x, y) + self._depth) % 20183
        return self._erosion[x, y]

    def type(self, x, y):
        return self.erosion(x, y) % 3

    def part_one(self):
        return sum(self.type(x, y) for x in range(0, self.target[0] + 1) for y in range(0, self.target[1] + 1))

    def gear_valid(self, x, y, gear):
        valid = None
        if self.type(x, y) == Cave.ROCKY:
            valid = Cave.CLIMBING | Cave.TORCH
        elif self.type(x, y) == Cave.WET:
            valid = Cave.CLIMBING | Cave.NEITHER
        elif self.type(x, y) == Cave.NARROW:
            valid = Cave.TORCH | Cave.NEITHER
        return valid & gear == gear

    def next_moves(self, x, y, equipment):
        for next_x, next_y in {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}:
            if next_x < 0 or next_y < 0 or next_y > self._depth:
                continue
            if self.gear_valid(next_x, next_y, equipment):
                yield (next_x, next_y, equipment, 1)
        for next_equipment in [Cave.NEITHER, Cave.TORCH, Cave.CLIMBING]:
            if self.gear_valid(x, y, next_equipment) and next_equipment != equipment:
                yield (x, y, next_equipment, 7)


def find_path(cave):
    seen = set()
    queue = defaultdict(set)
    queue[0].add((0, 0, Cave.TORCH))
    found = inf
    while min(queue.keys()) < found:
        lowest_cost = min(queue.keys())
        x, y, equipment = queue[lowest_cost].pop()
        seen.add((x, y, equipment))
        if len(queue[lowest_cost]) == 0:
            del queue[lowest_cost]
        for next_x, next_y, next_equipment, next_cost in cave.next_moves(x, y, equipment):
            cost = lowest_cost + next_cost
            if (next_x, next_y) == cave.target and next_equipment == Cave.TORCH:
                found = min(found, cost)
            if (next_x, next_y, next_equipment) not in seen:
                queue[cost].add((next_x, next_y, next_equipment))
    return found


# TEST = Cave(510, (10, 10))
# assert(TEST.type(0, 0) == Cave.ROCKY)
# assert(TEST.type(1, 0) == Cave.WET)
# assert(TEST.type(0, 1) == Cave.ROCKY)
# assert(TEST.type(1, 1) == Cave.NARROW)
# assert(TEST.type(10, 10) == Cave.ROCKY)
# assert(TEST.part_one() == 114)
# assert(find_path(TEST) == 45)

CAVE = Cave(*load_input('input.txt'))
print("Part One: {}".format(CAVE.part_one()))
print("Part Two: {}".format(find_path(CAVE)))

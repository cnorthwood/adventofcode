#!/usr/bin/env pypy3

INPUT = 369


def spinlock(l, position, i, steps):
    position = ((position + steps) % len(l)) + 1
    l.insert(position, i)
    return l, position


assert spinlock([0], 0, 1, 3) == ([0, 1], 1)
assert spinlock([0, 1], 1, 2, 3) == ([0, 2, 1], 1)
assert spinlock([0, 2, 1], 1, 3, 3) == ([0, 2, 3, 1], 2)


def repeat_spin(steps, times=2017):
    l = [0]
    position = 0
    for i in range(1, times + 1):
        l, position = spinlock(l, position, i, steps)
    return l[position + 1]


assert repeat_spin(3) == 638
print("Part One:", repeat_spin(INPUT))

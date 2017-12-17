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


test_spin = repeat_spin(3)
assert repeat_spin(3) == 638
part_one = repeat_spin(INPUT)
print("Part One:", repeat_spin(2017))


def spy_on(target, steps, times=50000000):
    target_value = None
    position = 0
    for i in range(1, times + 1):
        position = ((position + steps) % i) + 1
        if position == target:
            target_value = i
    return target_value


print("Part Two:", spy_on(1, INPUT))

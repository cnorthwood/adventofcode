#!/usr/bin/env python3
from sys import maxsize

INPUT = 289326


def ring_size(i):
    return (4 * (2 * i - 1)) - 4


def find_corners(ring_start, ring_i):
    ring_start -= 1
    quarter_size = ring_size(ring_i) // 4
    return ring_start + quarter_size, ring_start + quarter_size * 2, ring_start + quarter_size * 3


def find_ring(n):
    if n == 1:
        return 0
    ring_start = 1
    ring_end = 1
    ring_i = 0
    while n > ring_end:
        ring_i += 1
        ring_start = ring_end + 1
        ring_end += ring_size(ring_i)
    return ring_end + 1, find_corners(ring_start, ring_i)


def main(size):
    offsets = [None, (0, 0)]
    direction = (1, 0)
    location = (0, 0)
    ring_start = 2
    corners = (None, None, None)

    for n in range(2, size + 2):
        location = (location[0] + direction[0], location[1] + direction[1])
        offsets.append(location)

        # figure next direction
        if n == ring_start:
            direction = (0, 1)
            ring_start, corners = find_ring(n)
        elif n == corners[0]:
            direction = (-1, 0)
        elif n == corners[1]:
            direction = (0, -1)
        elif n == corners[2]:
            direction = (1, 0)

    return offsets


def steps_to_origin(n, offsets):
    return abs(offsets[n][0]) + abs(offsets[n][1])


offsets = main(INPUT)
assert steps_to_origin(1, offsets) == 0
assert steps_to_origin(12, offsets) == 3
assert steps_to_origin(23, offsets) == 2
assert steps_to_origin(1024, offsets) == 31

print("Part One:", steps_to_origin(INPUT, offsets))


def calculate(n):
    offsets = main(n)
    results = {
        (0, 0): 1,
    }
    for i in range(2, n + 1):
        x, y = offsets[i]
        results[(x, y)] = results.get((x - 1, y - 1), 0) \
            + results.get((x, y - 1), 0) \
            + results.get((x + 1, y - 1), 0) \
            + results.get((x - 1, y), 0) \
            + results.get((x + 1, y), 0) \
            + results.get((x - 1, y + 1), 0) \
            + results.get((x, y + 1), 0) \
            + results.get((x + 1, y + 1), 0)
    return results[offsets[n]]


assert calculate(1) == 1
assert calculate(2) == 1
assert calculate(3) == 2
assert calculate(4) == 4
assert calculate(5) == 5

for n in range(1, maxsize):
    if calculate(n) > INPUT:
        print("Part 2:", calculate(n))
        break

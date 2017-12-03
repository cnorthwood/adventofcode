#!/usr/bin/env python3

INPUT = 289326


def ring_size(i):
    return (4 * (2 * i - 1)) - 4


def middles(ring_start, ring_i):
    quarter_size = ring_size(ring_i) // 4
    first_middle = ring_start + ring_i - 2
    return first_middle, first_middle + quarter_size, first_middle + 2 * quarter_size, first_middle + 3 * quarter_size


def distance_to_closest_middle(n, middles):
    return min([
        abs(n - middles[0]),
        abs(n - middles[1]),
        abs(n - middles[2]),
        abs(n - middles[3]),
    ])


def distance(n):
    if n == 1:
        return 0
    ring_start = 1
    ring_end = 1
    ring_i = 0
    while n > ring_end:
        ring_i += 1
        ring_start = ring_end + 1
        ring_end += ring_size(ring_i)
    return ring_i - 1 + distance_to_closest_middle(n, middles(ring_start, ring_i))


assert distance(1) == 0
assert distance(12) == 3
assert distance(23) == 2
assert distance(1024) == 31

print("Part 1:", distance(INPUT))

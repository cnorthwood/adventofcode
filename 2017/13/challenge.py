#!/usr/bin/env python3


def scanner_location(depth, picosecond, ranges):
    if depth not in ranges:
        return None

    sequence = list(range(ranges[depth])) + list(range(ranges[depth] - 2, 0, -1))
    return sequence[picosecond % len(sequence)]


assert scanner_location(0, 0, {0: 3}) == 0
assert scanner_location(6, 6, {6: 4}) == 0


def severity(packet_depth, picosecond, ranges):
    if scanner_location(packet_depth, picosecond, ranges) == 0:
        return ranges[packet_depth] * packet_depth
    else:
        return 0


def total_severity(ranges):
    return sum(severity(picosecond, picosecond, ranges) for picosecond in range(max(ranges.keys()) + 1))


assert total_severity({0: 3, 1: 2, 4: 4, 6: 4}) == 24

with open('input.txt') as input_file:
    RANGES = {}
    for line in input_file.read().strip().splitlines():
        depth, rng = list(map(int, line.split(': ')))
        RANGES[depth] = rng

print("Part One:", total_severity(RANGES))

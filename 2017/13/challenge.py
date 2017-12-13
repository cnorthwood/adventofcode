#!/usr/bin/env python3

from itertools import count

TEST_RANGES = {0: 3, 1: 2, 4: 4, 6: 4}


def scanner_location(depth, picosecond, ranges):
    if depth not in ranges:
        return None

    sequence = list(range(ranges[depth])) + list(range(ranges[depth] - 2, 0, -1))
    return sequence[picosecond % len(sequence)]


assert scanner_location(0, 0, TEST_RANGES) == 0
assert scanner_location(6, 6, TEST_RANGES) == 0


def severity(packet_depth, picosecond, ranges):
    if scanner_location(packet_depth, picosecond, ranges) == 0:
        return ranges[packet_depth] * packet_depth
    else:
        return 0


def total_severity(ranges,):
    return sum(severity(picosecond, picosecond, ranges) for picosecond in range(max(ranges.keys()) + 1))


assert total_severity(TEST_RANGES) == 24


def is_caught(ranges, delay):
    for picosecond in range(max(ranges.keys()) + 1):
        if scanner_location(picosecond, picosecond + delay, ranges) == 0:
            return True
    else:
        return False


def find_crossing_delay(ranges):
    for delay in count():
        if not is_caught(ranges, delay):
            return delay


assert find_crossing_delay(TEST_RANGES) == 10


with open('input.txt') as input_file:
    RANGES = {}
    for line in input_file.read().strip().splitlines():
        depth, rng = list(map(int, line.split(': ')))
        RANGES[depth] = rng

print("Part One:", total_severity(RANGES))
print("Part Two:", find_crossing_delay(RANGES))

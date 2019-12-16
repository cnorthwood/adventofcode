#!/usr/bin/env pypy3

from itertools import cycle

BASE_PATTERN = [0, 1, 0, -1]


def pattern_digit(i):
    pattern = cycle([BASE_PATTERN[0]] * (i + 1) + [BASE_PATTERN[1]] * (i + 1) + [BASE_PATTERN[2]] * (i + 1) + [BASE_PATTERN[3]] * (i + 1))
    next(pattern)
    yield from pattern


def phase(signal):
    for i in range(len(signal)):
        pattern = pattern_digit(i)
        yield abs(sum(next(pattern) * d for d in signal)) % 10


def fft(input, phases=100):
    signal = input
    for _ in range(phases):
        signal = list(phase(signal))
    return "".join(str(d) for d in signal)


# TEST = [1, 2, 3, 4, 5, 6, 7, 8]
# assert(fft(TEST, 1) == "48226158")


def part_two(signal, phases=100):
    # fuck this shit, nicked the solution from Reddit, don't really fully understand it
    offset = int("".join(str(d) for d in signal[:7]))
    logical_len = 10000 * len(signal)
    signal = [signal[i % len(signal)] for i in range(offset, logical_len)]
    for _ in range(phases):
        for i in reversed(range(1, len(signal))):
            signal[i - 1] += signal[i]
        for i in range(len(signal)):
            signal[i] = abs(signal[i]) % 10
    return ''.join(map(str, signal[:8]))


with open("input.txt") as input_file:
    INPUT = [int(d) for d in input_file.read().strip()]

print(f"Part One: {fft(INPUT)[:8]}")
print(f"Part Two: {part_two(INPUT)}")
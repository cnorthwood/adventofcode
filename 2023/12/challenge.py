#!/usr/bin/env python3

from itertools import product
from multiprocessing import cpu_count, Pool
import re


def load_input(filename):
    with open(filename) as input_file:
        for line in input_file:
            pattern, sequence = line.split()
            yield pattern, [int(d) for d in sequence.split(",")]


def is_valid_pattern(pattern, sequence):
    matches = re.findall(r'#+', pattern)
    return [len(m) for m in matches] == sequence


def possibilities(pattern):
    unknown_indexes = [match.start() for match in re.finditer(r"\?", pattern)]
    for replacements in product("#.", repeat=len(unknown_indexes)):
        possibility = list(pattern)
        for i, c in enumerate(replacements):
            possibility[unknown_indexes[i]] = c
        yield "".join(possibility)


def num_valid_possibilities(pattern, sequence):
    return sum(1 for possibility in possibilities(pattern) if is_valid_pattern(possibility, sequence))


def unfold_inputs(lines, times=5):
    for pattern, sequence in lines:
        yield "?".join([pattern] * 5), sequence * times


assert(is_valid_pattern("#.#.###.", [1, 1, 3]))
assert(num_valid_possibilities("???.###", [1, 1, 3]) == 1)
assert(num_valid_possibilities(".??..??...?##.", [1, 1, 3]) == 4)
assert(num_valid_possibilities("?#?#?#?#?#?#?#?", [1, 3, 1, 6]) == 1)
assert(num_valid_possibilities("????.#...#...", [4, 1, 1]) == 1)
assert(num_valid_possibilities("????.######..#####.", [1, 6, 5]) == 4)
assert(num_valid_possibilities("?###????????", [3, 2, 1]) == 10)


def parallelise(inputs):
    with Pool(processes=cpu_count()) as pool:
        return sum(pool.starmap(num_valid_possibilities, inputs))


if __name__ == "__main__":
    INPUT = list(load_input("input.txt"))
    print(f"Part One: {parallelise(INPUT)}")
    # print(f"Part Two: {sum(parallelise(unfold_inputs(INPUT)))}")
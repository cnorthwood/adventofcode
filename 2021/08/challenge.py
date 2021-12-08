#!/usr/bin/env python3


def load_input(filename):
    with open(filename) as input_file:
        for line in input_file:
            wires, output = line.strip().split(" | ")
            yield [frozenset(wire) for wire in wires.split()], [
                frozenset(digit) for digit in output.split()
            ]


POSSIBLE_POSITIONS = frozenset("abcdefg")
UNAMBIGUOUS_DIGITS = frozenset("1478")
UNSCRAMBLED = {
    "0": frozenset("abcefg"),
    "1": frozenset("cf"),
    "2": frozenset("acdeg"),
    "3": frozenset("acdfg"),
    "4": frozenset("bcdf"),
    "5": frozenset("abdfg"),
    "6": frozenset("abdefg"),
    "7": frozenset("acf"),
    "8": frozenset("abcdefg"),
    "9": frozenset("abcdfg"),
}
INPUT = list(load_input("input.txt"))


def work_out_mapping(wirings):
    combinations = {wire: set(POSSIBLE_POSITIONS) for wire in POSSIBLE_POSITIONS}
    remaining_wirings = set(wirings)
    while any(len(possibility) > 1 for possibility in combinations.values()):
        for possibility in frozenset(remaining_wirings):
            if len(possibility) == 2:
                # this is 1
                combinations["c"] &= possibility
                combinations["f"] &= possibility
            elif len(possibility) == 4:
                # this is 4
                combinations["b"] &= possibility
                combinations["c"] &= possibility
                combinations["d"] &= possibility
                combinations["f"] &= possibility
            elif len(possibility) == 3:
                # this is 7
                combinations["a"] &= possibility
                combinations["c"] &= possibility
                combinations["f"] &= possibility
            elif len(possibility) == 7:
                # this is 8
                combinations["a"] &= possibility
                combinations["b"] &= possibility
                combinations["c"] &= possibility
                combinations["d"] &= possibility
                combinations["e"] &= possibility
                combinations["f"] &= possibility
                combinations["g"] &= possibility
            elif len(possibility) == 6:
                # this could be 0, 6 or 9
                combinations["a"] &= possibility
                combinations["b"] &= possibility
                combinations["f"] &= possibility
                combinations["g"] &= possibility
            elif len(possibility) == 5:
                # this could be 2, 3 or 5
                combinations["a"] &= possibility
                combinations["d"] &= possibility
                combinations["g"] &= possibility

        # now where we've figured one exactly then remove it from elsewhere
        for wire, possibilities in combinations.items():
            if len(possibilities) > 1:
                continue
            if len(possibilities) == 0:
                raise ValueError("oh no")
            confirmed = next(iter(possibilities))
            for other_wire, possibilities in combinations.items():
                if wire == other_wire:
                    continue
                possibilities.discard(confirmed)

    mappings = {wire: positions.pop() for wire, positions in combinations.items()}
    return {
        digit: {mappings[wire] for wire in wirings}
        for digit, wirings in UNSCRAMBLED.items()
    }


def decode(combinations, output):
    decoded = ""
    for output_wiring in output:
        for digit, digit_wiring in combinations.items():
            if digit_wiring == output_wiring:
                decoded += digit
                break
        else:
            raise ValueError(f"could not decode {output_wiring}")
    return int(decoded)


print(f"Part One: {sum(sum(1 for digit in output if len(digit) in (len(UNSCRAMBLED[digit]) for digit in UNAMBIGUOUS_DIGITS)) for _, output in INPUT)}")
print(f"Part Two: {sum(decode(work_out_mapping(wirings), output) for wirings, output in INPUT)}")

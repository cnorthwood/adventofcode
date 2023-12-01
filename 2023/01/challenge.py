#!/usr/bin/env python3

import re

VALUES = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def extract_digits(line):
    match = re.findall(r"\d", line)
    return int(match[0] + match[-1])


def extract_wordy_digits(line):
    # the answers can overlap, so let's use the negative lookahead operator to make sure we don't consume when we match
    match = re.findall(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", line)
    return int(VALUES.get(match[0], match[0]) + VALUES.get(match[-1], match[-1]))


assert(extract_wordy_digits("two1nine") == 29)
assert(extract_wordy_digits("eightwothree") == 83)
assert(extract_wordy_digits("abcone2threexyz") == 13)
assert(extract_wordy_digits("xtwone3four") == 24)
assert(extract_wordy_digits("4nineeightseven2") == 42)
assert(extract_wordy_digits("zoneight234") == 14)
assert(extract_wordy_digits("7pqrstsixteen") == 76)
# example test cases nicked from Reddit, sneaky day 1!
assert(extract_wordy_digits("eighthree") == 83)
assert(extract_wordy_digits("sevenine") == 79)


with open("input.txt") as input_file:
    LINES = [line.strip() for line in input_file.readlines()]

print(f"Part One: {sum(extract_digits(line) for line in LINES)}")
print(f"Part Two: {sum(extract_wordy_digits(line) for line in LINES)}")

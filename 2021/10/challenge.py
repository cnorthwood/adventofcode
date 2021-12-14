#!/usr/bin/env python3

OPPOSITES = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

CHECKER_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

COMPLETER_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

with open("input.txt") as input_file:
    INPUT = [line.strip() for line in input_file]


def leftover_score(leftover):
    score = 0
    for c in reversed(leftover):
        score *= 5
        score += COMPLETER_SCORE[c]
    return score


def corrupt_and_complete_scores(line):
    nest = []
    for c in line:
        if c in OPPOSITES.keys():
            nest.append(OPPOSITES[c])
        else:
            expected = nest.pop()
            if c != expected:
                return CHECKER_SCORE[c], 0
    return 0, leftover_score(nest)


SCORES = [corrupt_and_complete_scores(line) for line in INPUT]
print(f"Part One: {sum(corrupt for corrupt, completion in SCORES)}")
AUTO_COMPLETE_SCORES = [completion for corrupt, completion in SCORES if corrupt == 0]
AUTO_COMPLETE_SCORES.sort()
print(f"Part Two: {AUTO_COMPLETE_SCORES[len(AUTO_COMPLETE_SCORES) // 2]}")

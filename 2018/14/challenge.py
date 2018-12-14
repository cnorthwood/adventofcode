#!/usr/bin/env pypy3


def generate_new_recipes(elves, scores):
    return list(map(int, str(sum(scores[elf] for elf in elves))))


def step(elves, scores):
    for new_recipe in generate_new_recipes(elves, scores):
        scores.append(new_recipe)
    return [(elf + scores[elf] + 1) % len(scores) for elf in elves], scores


def target(n):
    elves, scores = [0, 1], [3, 7]
    while len(scores) < n + 10:
        elves, scores = step(elves, scores)
    return ''.join(map(str, scores[n:n+10]))


assert(target(9) == '5158916779')
assert(target(5) == '0124515891')
assert(target(18) == '9251071085')
assert(target(2018) == '5941429882')

with open('input.txt') as input_file:
    INPUT = input_file.read().strip()

print("Part One: {}".format(target(int(INPUT))))


def find_appearance(recipe):
    recipe = [int(c) for c in recipe]
    elves, scores = [0, 1], [3, 7]
    while scores[-len(recipe):] != recipe and scores[-len(recipe)-1:-1] != recipe:
        elves, scores = step(elves, scores)
    if scores[-len(recipe):] != recipe:
        scores = scores[:-1]
    return len(scores) - len(recipe)


assert(find_appearance('51589') == 9)
assert(find_appearance('01245') == 5)
assert(find_appearance('92510') == 18)
assert(find_appearance('59414') == 2018)

print("Part Two: {}".format(find_appearance(INPUT)))

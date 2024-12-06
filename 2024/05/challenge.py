#!/usr/bin/env pypy3 -S

from itertools import filterfalse, permutations


def load_input(filename):
    rules = []
    pages = []

    input_section = 1
    with open(filename) as input_file:
        for line in input_file:
            if not line.strip():
                input_section += 1
                continue
            if input_section == 1:
                rules.append(tuple(map(int, line.strip().split("|"))))
            if input_section == 2:
                pages.append(list(map(int, line.strip().split(","))))

    return rules, pages


def valid_rule_on_page(page, rule):
    if rule[0] not in page or rule[1] not in page:
        return True

    return page.index(rule[0]) < page.index(rule[1])


def valid_page(page):
    return all(valid_rule_on_page(page, rule) for rule in RULES)


def reordered_page(page):
    shuffled_page = page[:]
    while not valid_page(shuffled_page):
        for rule in RULES:
            if not valid_rule_on_page(shuffled_page, rule):
                i = shuffled_page.index(rule[0])
                j = shuffled_page.index(rule[1])
                shuffled_page[i] = rule[1]
                shuffled_page[j] = rule[0]
    return shuffled_page


RULES, PAGES = load_input("input.txt")
valid_pages = list(filter(valid_page, PAGES))
invalid_pages = list(filterfalse(valid_page, PAGES))

print(f"Part One: {sum(page[len(page) // 2] for page in valid_pages)}")
print(f"Part Two: {sum(reordered_page(page)[len(page) // 2] for page in invalid_pages)}")

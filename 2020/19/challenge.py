#!/usr/bin/env python3
import re
from functools import cache
from itertools import product


def load_input(input_file):
    mode = "rules"
    rules = {}
    messages = []
    for line in input_file.readlines():
        if line.strip() == "":
            mode = "messages"
        elif mode == "rules":
            rule_id, rule_body = line.strip().split(": ")
            rules[rule_id] = [rule.split() for rule in rule_body.split(" | ")]
        elif mode == "messages":
            messages.append(line.strip())
    return rules, messages


def generate_strings(rule_id, rules):
    for rule in rules[rule_id]:
        if rule[0].startswith('"'):
            yield rule[0].strip('"')
        else:
            for s in product(*(generate_strings(part, rules) for part in rule)):
                yield ''.join(s)


@cache
def build_regex_str(rule_id):
    if RULES[rule_id][0][0].startswith('"'):
        return RULES[rule_id][0][0].strip('"')
    else:
        return f"({'|'.join(''.join(build_regex_str(part) for part in rule) for rule in RULES[rule_id])})"


with open("input.txt") as input_file:
    RULES, MESSAGES = load_input(input_file)
# POSSIBLE_MESSAGES = frozenset(generate_strings("0", RULES))
# print(f"Part One: {sum(1 for s in MESSAGES if s in POSSIBLE_MESSAGES)}")
REGEX = re.compile(build_regex_str("0") + "$")
print(f"Part One: {sum(1 for s in MESSAGES if REGEX.match(s))}")

UPDATED_RULE_8 = f"{build_regex_str('42')}+"
# slight hack to work around balancing in a regexp
UPDATED_RULE_11 = "(" + "|".join(build_regex_str("42") + "{" + str(n) + "}" + build_regex_str("31") + "{" + str(n) + "}" for n in range(1, 5)) + ")"
PART_TWO_REGEX = re.compile(f"{UPDATED_RULE_8}{UPDATED_RULE_11}$")
print(f"Part Two: {sum(1 for s in MESSAGES if PART_TWO_REGEX.match(s))}")

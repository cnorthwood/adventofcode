#!/usr/bin/env python3

def parse_rules(lines):
    rules = {}
    for line in lines:
        outer, inners = line.strip(".\n").split(" contain ")
        if outer.endswith(" bag"):
            outer = outer[:-4]
        elif outer.endswith(" bags"):
            outer = outer[:-5]
        rules[outer] = []
        if inners == "no other bags":
            continue
        for inner in inners.split(", "):
            num, bag_type = inner.split(maxsplit=1)
            if bag_type.endswith(" bag"):
                bag_type = bag_type[:-4]
            elif bag_type.endswith(" bags"):
                bag_type = bag_type[:-5]
            num = int(num)
            rules[outer].append((num, bag_type))
    return rules


def find_containers(needle, rule_tree):
    result = set()
    for outer, inners in rule_tree.items():
        for val, inner in inners:
            if inner == needle:
                result.add(outer)
                result |= find_containers(outer, rule_tree)
    return result


def find_contained_numbers(root, rule_tree):
    return sum(v + (v * find_contained_numbers(inner, rule_tree)) for v, inner in rule_tree[root])


with open("input.txt") as input_file:
    INPUT = parse_rules(input_file.readlines())

print(f"Part One: {len(find_containers('shiny gold', INPUT))}")
print(f"Part Two: {find_contained_numbers('shiny gold', INPUT)}")

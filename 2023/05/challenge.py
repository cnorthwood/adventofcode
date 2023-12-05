#!/usr/bin/env python3

from collections import defaultdict
import re


def load_map(filename):
    with open(filename) as input_file:
        first_line = next(input_file)
        initial_seeds = [("seed", int(seed)) for seed in first_line.split(": ")[1].split()]
        mappings = defaultdict(dict)
        for line in input_file:
            if not line.strip():
                continue

            if header_match := re.match(r'(?P<source>\w+)-to-(?P<destination>\w+) map:', line):
                source_category = header_match.group("source")
                destination_category = header_match.group("destination")
                continue

            destination_start, source_start, range_length = map(int, line.split())
            mappings[source_category][(source_start, source_start + range_length)] = (destination_category, destination_start)

    return initial_seeds, mappings


def find_requirement(item, mappings):
    category, item_number = item
    for (start, end), (destination_category, destination_start) in mappings[category].items():
        if start <= item_number < end:
            return destination_category, destination_start + (item_number - start)
    return destination_category, item_number


def find_location(start_item, mappings):
    category, item_number = start_item
    while category != "location":
        category, item_number = find_requirement((category, item_number), mappings)
    return item_number


INITIAL_SEEDS, MAPPINGS = load_map("input.txt")
print(f"Part One: {min(find_location(seed, MAPPINGS) for seed in INITIAL_SEEDS)}")

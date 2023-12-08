#!/usr/bin/env python3

from collections import defaultdict
import re


def load_map(filename):
    with open(filename) as input_file:
        first_line = next(input_file)
        initial_seeds = [int(seed) for seed in first_line.split(": ")[1].split()]
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


def find_requirement(item):
    category, item_number = item
    for (start, end), (destination_category, destination_start) in MAPPINGS[category].items():
        if start <= item_number < end:
            return destination_category, destination_start + (item_number - start)
    return destination_category, item_number


def find_location(seed):
    category = "seed"
    item_number = seed
    while category != "location":
        category, item_number = find_requirement((category, item_number))
    return item_number


# this returns, for a particular interval, where all the subintervals are
def interval_partition_points(category, start, end):
    if category == "location":
        return {start}

    next_category = next(iter(MAPPINGS[category].values()))[0]
    subranges = {(start, end): 0}
    for (sub_start, sub_end), sub_d in subranges.copy().items():
        for (interval_start, interval_end), (next_category, target_start) in MAPPINGS[category].items():
            d = target_start - interval_start

            # start of interval overlaps with this subrange
            if interval_start <= sub_start < interval_end < sub_end:
                subranges.pop((sub_start, sub_end), None)
                subranges[(sub_start, interval_end)] = d
                subranges[(interval_end, sub_end)] = sub_d

            # whole of interval overlaps with this subrange
            if sub_start < interval_start < interval_end < sub_end:
                subranges.pop((sub_start, sub_end), None)
                subranges[(sub_start, interval_start - 1)] = sub_d
                subranges[(interval_start, interval_end)] = d
                subranges[(interval_end + 1, sub_end)] = sub_d

            # end of interval overlaps with this subrange
            if sub_start < interval_start < sub_end <= interval_end:
                subranges.pop((sub_start, sub_end), None)
                subranges[(sub_start, interval_start - 1)] = sub_d
                subranges[(interval_start, sub_end)] = d

            # interval sits over this whole subrange
            if interval_start <= sub_start < sub_end <= interval_end:
                subranges[(sub_start, sub_end)] = d

    return {n - d for (sub_start, sub_end), d in subranges.items() for n in interval_partition_points(next_category, sub_start + d, sub_end + d)}


def part2_seeds(initial_seeds):
    seed_ranges = [(start, start + n) for start, n in zip(initial_seeds[::2], initial_seeds[1::2])]
    starts_to_consider = set()
    for start, end in seed_ranges:
        starts_to_consider |= interval_partition_points("seed", start, end)
    return starts_to_consider


INITIAL_SEEDS, MAPPINGS = load_map("input.txt")
print(f"Part One: {min(find_location(seed) for seed in INITIAL_SEEDS)}")
print(f"Part Two: {min(find_location(seed) for seed in part2_seeds(INITIAL_SEEDS))}")

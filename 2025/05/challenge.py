#!/usr/bin/env python3


def load_input(filename):
    with open(filename) as input_file:
        fresh_ranges = set()
        while (line := input_file.readline().strip()):
            start, end = line.split("-")
            fresh_ranges.add((int(start), int(end)))
        ingredient_ids = {int(line.strip()) for line in input_file.readlines()}
    return fresh_ranges, ingredient_ids


def is_fresh(ingredient_id, fresh_ranges):
    for start, end in fresh_ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def merge_ranges(ranges):
    merged_ranges = []

    for range_to_be_considered in sorted(ranges):
        if len(merged_ranges) == 0:
            # base case - no ranges have been merged yet so add our first one
            merged_ranges.append(range_to_be_considered)
        else:
            previous_start, previous_end = merged_ranges[-1]
            range_start, range_end = range_to_be_considered
            if range_start <= previous_end:
                # this range overlaps with the last one we added so we can merge it - if it's wider, then we set it to the new end
                if range_end > previous_end:
                    merged_ranges[-1] = (previous_start, range_end)
            else:
                # this can not be merged, and because we've sorted these no range after it possibly can so create a new range
                merged_ranges.append(range_to_be_considered)

    return merged_ranges


FRESH_RANGES, INGREDIENT_IDS = load_input("input.txt")
SIMPLIFIED_RANGES = merge_ranges(FRESH_RANGES)

print(f"Part One: {sum(1 for ingredient_id in INGREDIENT_IDS if is_fresh(ingredient_id, SIMPLIFIED_RANGES))}")
print(f"Part Two: {sum(end - start + 1 for start, end in SIMPLIFIED_RANGES)}")

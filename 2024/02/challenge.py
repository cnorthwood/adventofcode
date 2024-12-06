#!/usr/bin/env python3 -S

def all_descending(ns):
    return all(a > b for a, b in zip(ns, ns[1:]))

def all_ascending(ns):
    return all(a < b for a, b in zip(ns, ns[1:]))

def no_big_steps(ns):
    return all(1 <= abs(a-b) <= 3 for a, b in zip(ns, ns[1:]))

def safe(ns):
    return no_big_steps(ns) and (all_descending(ns) or all_ascending(ns))

def dampened_safe(ns):
    return safe(ns) or any(safe(ns[:i] + ns[i+1:]) for i in range(len(ns)))


with open("input.txt") as input_file:
    REPORTS = [list(map(int, line.split())) for line in input_file]

print(f"Part One: {sum(1 for report in REPORTS if safe(report))}")
print(f"Part Two: {sum(1 for report in REPORTS if dampened_safe(report))}")

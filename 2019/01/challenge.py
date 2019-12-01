#!/usr/bin/env pypy3


def fuel_for_mass(mass):
    return max(0, mass // 3 - 2)


def total_fuel_requirement(initial_mass):
    masses = [initial_mass]
    while masses[-1] > 0:
        masses.append(fuel_for_mass(masses[-1]))
    return sum(masses[1:])


assert(fuel_for_mass(12) == 2)
assert(fuel_for_mass(14) == 2)
assert(fuel_for_mass(1969) == 654)
assert(fuel_for_mass(100756) == 33583)

assert(total_fuel_requirement(14) == 2)
assert(total_fuel_requirement(1969) == 966)
assert(total_fuel_requirement(100756) == 50346)

with open("input.txt") as puzzle_input:
    masses = [int(line) for line in puzzle_input]

print(f"Part One: {sum(map(fuel_for_mass, masses))}")
print(f"Part Two: {sum(map(total_fuel_requirement, masses))}")

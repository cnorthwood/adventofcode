#!/usr/bin/env python3


def populate_locations(line):
    locations = set()
    distances = {}
    x, y = 0, 0
    steps = 0
    for instruction in line.split(","):
        movement = int(instruction[1:])
        if instruction[0] == "R":
            for _ in range(movement):
                x += 1
                steps += 1
                locations.add((x, y))
                if (x, y) not in distances:
                    distances[(x, y)] = steps
        elif instruction[0] == "L":
            for _ in range(movement):
                x -= 1
                steps += 1
                locations.add((x, y))
                if (x, y) not in distances:
                    distances[(x, y)] = steps
        elif instruction[0] == "D":
            for _ in range(movement):
                y -= 1
                steps += 1
                locations.add((x, y))
                if (x, y) not in distances:
                    distances[(x, y)] = steps
        elif instruction[0] == "U":
            for _ in range(movement):
                y += 1
                steps += 1
                locations.add((x, y))
                if (x, y) not in distances:
                    distances[(x, y)] = steps
        else:
            raise Exception(f"Unknown instruction {instruction}")
    return locations, distances


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_closest(locations):
    overlapping_points = set.intersection(*locations)
    return min(manhattan((0, 0), point) for point in overlapping_points)


def find_minimum_steps(location_and_distances):
    (locations_a, distances_a), (locations_b, distances_b) = location_and_distances
    overlapping_points = set.intersection(locations_a, locations_b)
    return min(distances_a[location] + distances_b[location] for location in overlapping_points)


with open("input.txt") as input_file:
    INPUT = [populate_locations(line) for line in input_file.readlines()]

print(f"Part One: {find_closest(locations for locations, distances in INPUT)}")
print(f"Part Two: {find_minimum_steps(INPUT)}")

#!/usr/bin/env -S pypy3 -S

def load_input(input_filename):
    with open(input_filename) as input_file:
        return {(x, y): c for y, line in enumerate(input_file) for x, c in enumerate(line.strip())}


def fill_partition(field, plant, loc, partition):
    for neighbour in neighbours(loc):
        if field.get(neighbour) == plant and neighbour not in partition:
            partition.add(neighbour)
            fill_partition(field, plant, neighbour, partition)


def partition_field(field):
    partitions = []
    field = field.copy()
    while len(field):
        start_loc = next(iter(field))
        plant = field[start_loc]
        partition = {start_loc}
        fill_partition(field, plant, start_loc, partition)
        for square in partition:
            del field[square]
        partitions.append((plant, partition))
    return partitions


def area(partition):
    return len(partition)


def neighbours(square):
    x, y = square
    yield x - 1, y
    yield x + 1, y
    yield x, y - 1
    yield x, y + 1


def perimeter(partition):
    length = 0
    for square in partition:
        for neighbour in neighbours(square):
            if neighbour not in partition:
                length += 1
    return length


INPUT = load_input("input.txt")

print(f"Part One: {sum(area(partition) * perimeter(partition) for _, partition in partition_field(INPUT))}")

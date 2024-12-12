#!/usr/bin/env -S pypy3 -S

from enum import Enum

class Directions(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Diagonals(Enum):
    TOP_LEFT = (-1, -1)
    TOP_RIGHT = (1, -1)
    BOTTOM_LEFT = (-1, 1)
    BOTTOM_RIGHT = (1, 1)


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
        partitions.append(partition)
    return partitions


def area(partition):
    return len(partition)


def neighbour(square, direction):
    return square[0] + direction.value[0], square[1] + direction.value[1]


def neighbours(square):
    for direction in Directions:
        yield neighbour(square, direction)


def perimeter(partition):
    length = 0
    for square in partition:
        for neighbour in neighbours(square):
            if neighbour not in partition:
                length += 1
    return length


def num_neighbours(square, partition):
    return sum(1 for neighbour in neighbours(square) if neighbour in partition)


def num_corners(square, partition):
    n = 0
    # inner corner, top left
    if (neighbour(square, Directions.LEFT) in partition and
            neighbour(square, Directions.UP) in partition and
            neighbour(square, Diagonals.TOP_LEFT) not in partition):
        n += 1
    # inner corner, top right
    if (neighbour(square, Directions.RIGHT) in partition and
            neighbour(square, Directions.UP) in partition and
            neighbour(square, Diagonals.TOP_RIGHT) not in partition):
        n += 1
    # inner corner, bottom left
    if (neighbour(square, Directions.LEFT) in partition and
            neighbour(square, Directions.DOWN) in partition and
            neighbour(square, Diagonals.BOTTOM_LEFT) not in partition):
        n += 1
    # inner corner, bottom right
    if (neighbour(square, Directions.RIGHT) in partition and
            neighbour(square, Directions.DOWN) in partition and
            neighbour(square, Diagonals.BOTTOM_RIGHT) not in partition):
        n += 1
    # outer corner, top left
    if (neighbour(square, Directions.LEFT) not in partition and
            neighbour(square, Directions.UP) not in partition):
        n += 1
    # outer corner, top right
    if (neighbour(square, Directions.RIGHT) not in partition and
            neighbour(square, Directions.UP) not in partition):
        n += 1
    # outer corner, bottom left
    if (neighbour(square, Directions.LEFT) not in partition and
            neighbour(square, Directions.DOWN) not in partition):
        n += 1
    # outer corner, bottom right
    if (neighbour(square, Directions.RIGHT) not in partition and
            neighbour(square, Directions.DOWN) not in partition):
        n += 1
    return n


def num_sides(partition):
    sides = 0
    for square in partition:
        sides += num_corners(square, partition)

    return sides

# assert(num_sides({(1,1)}) == 4)
# assert(num_sides({(1,1), (1,2)}) == 4)
# assert(num_sides({(1,1), (1,2), (2, 2)}) == 6)
# assert(num_sides({(1,1), (1,2), (2, 2), (2, 3)}) == 8)
# assert(num_sides({(1,1), (1,2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)}) == 8)
# assert(num_sides({(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (5, 2), (5, 3), (4, 3), (3, 3), (3, 4), (4, 4), (5, 4), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (1, 2), (2, 2), (2, 1), (1, 1), (0, 1)}) == 12)


PARTITIONS = partition_field(load_input("input.txt"))

print(f"Part One: {sum(area(partition) * perimeter(partition) for partition in PARTITIONS)}")
print(f"Part Two: {sum(area(partition) * num_sides(partition) for partition in PARTITIONS)}")

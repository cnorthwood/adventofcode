#!/usr/bin/env python3

def parse_line(line):
    line = iter(line.strip())
    try:
        while c := next(line):
            if c == "s" or c == "n":
                c += next(line)
            yield c
    except StopIteration:
        pass


def follow_direction(coord, direction):
    q, r = coord
    if direction == "w":
        return q - 1, r
    elif direction == "e":
        return q + 1, r
    elif direction == "se":
        return q, r + 1
    elif direction == "sw":
        return q - 1, r + 1
    elif direction == "ne":
        return q + 1, r - 1
    elif direction == "nw":
        return q, r - 1
    else:
        raise ValueError(f"unrecognised direction {direction}")


def follow_path(path):
    coord = 0, 0
    for direction in path:
        coord = follow_direction(coord, direction)
    return coord


def renovate(paths):
    black_tiles = set()
    for path in paths:
        end = follow_path(path)
        if end in black_tiles:
            black_tiles.remove(end)
        else:
            black_tiles.add(end)
    return black_tiles


def neighbours(tile):
    return {follow_direction(tile, direction) for direction in ("w", "e", "se", "sw", "ne", "nw")}


def iterate(black_tiles):
    next_day = set()
    for tile in black_tiles:
        if 0 < len(black_tiles & neighbours(tile)) <= 2:
            next_day.add(tile)
        for neighbour in neighbours(tile):
            if neighbour not in black_tiles and len(black_tiles & neighbours(neighbour)) == 2:
                next_day.add(neighbour)
    return next_day


with open("input.txt") as input_file:
    INPUT = [list(parse_line(line)) for line in input_file.readlines() if line]
grid = renovate(INPUT)
print(f"Part One: {len(grid)}")
for _ in range(100):
    grid = iterate(grid)
print(f"Part Two: {len(grid)}")

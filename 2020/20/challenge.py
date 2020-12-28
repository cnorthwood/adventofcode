#!/usr/bin/env python3

from math import prod

SQUARE_SIZE = 10


def parse_tiles(input_file):
    tiles = {}
    this_tile = set()
    for line in input_file.readlines():
        if line.startswith("Tile"):
            if this_tile:
                tiles[this_tile_id] = this_tile
            this_tile_id = int(line.strip()[5:].strip(":"))
            this_tile = set()
            y = 0
            continue
        for x, c in enumerate(line.strip()):
            if c == "#":
                this_tile.add((x, y))
        y += 1
    tiles[this_tile_id] = this_tile
    return tiles


def edges(tile):
    top = 0
    bottom = 0
    left = 0
    right = 0
    topr = 0
    bottomr = 0
    leftr = 0
    rightr = 0
    for xy in range(SQUARE_SIZE):
        if (xy, 0) in tile:
            top |= 1 << xy
            topr |= 1 << SQUARE_SIZE - 1 - xy
        if (xy, SQUARE_SIZE - 1) in tile:
            bottom |= 1 << xy
            bottomr |= 1 << SQUARE_SIZE - 1 - xy
        if (0, xy) in tile:
            left |= 1 << xy
            leftr |= 1 << SQUARE_SIZE - 1 - xy
        if (SQUARE_SIZE - 1, xy) in tile:
            right |= 1 << xy
            rightr |= 1 << SQUARE_SIZE - 1 - xy
    return frozenset((
        top, bottom, left, right,
        topr, bottomr, leftr, rightr,
    ))


def neighbours(tile_id, all_edges):
    return {other_id for other_id, other_edges in all_edges.items()
            if tile_id != other_id and len(all_edges[tile_id] & other_edges) > 0}


with open("input.txt") as input_file:
    TILES = parse_tiles(input_file)
EDGES = {tile_id: edges(tile) for tile_id, tile in TILES.items()}

print(f"Part One: {prod(tile_id for tile_id in TILES.keys() if len(neighbours(tile_id, EDGES)) == 2)}")

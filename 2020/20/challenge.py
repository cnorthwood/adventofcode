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
    top = set()
    bottom = set()
    left = set()
    right = set()
    topr = set()
    bottomr = set()
    leftr = set()
    rightr = set()
    for xy in range(SQUARE_SIZE):
        if (xy, 0) in tile:
            top.add(xy)
            topr.add(SQUARE_SIZE - 1 - xy)
        if (xy, SQUARE_SIZE - 1) in tile:
            bottom.add(xy)
            bottomr.add(SQUARE_SIZE - 1 - xy)
        if (0, xy) in tile:
            left.add(xy)
            leftr.add(SQUARE_SIZE - 1 - xy)
        if (SQUARE_SIZE - 1, xy) in tile:
            right.add(xy)
            rightr.add(SQUARE_SIZE - 1 - xy)
    return frozenset((
        frozenset(top), frozenset(bottom), frozenset(left), frozenset(right),
        frozenset(topr), frozenset(bottomr), frozenset(leftr), frozenset(rightr),
    ))


def neighbours(tile_id, all_edges):
    return {other_id for other_id, other_edges in all_edges.items() if tile_id != other_id and len(all_edges[tile_id] & other_edges) > 0}


with open("input.txt") as input_file:
    TILES = parse_tiles(input_file)
EDGES = {tile_id: edges(tile) for tile_id, tile in TILES.items()}
NEIGHBOURS = {tile_id: neighbours(tile_id, EDGES) for tile_id in TILES.keys()}
print(f"Part One: {prod(tile_id for tile_id, neighbours in NEIGHBOURS.items() if len(neighbours) == 2)}")

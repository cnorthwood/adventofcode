#!/usr/bin/env python3

from itertools import chain

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


def rotate(tile):
    return frozenset((-y % SQUARE_SIZE, x) for x, y in tile)


def flip_v(tile):
    return frozenset((x, -y % SQUARE_SIZE) for x, y in tile)


def flip_h(tile):
    return frozenset((-x % SQUARE_SIZE, y) for x, y in tile)


def variants(tile):
    yield frozenset(tile)
    tile90 = rotate(tile)
    yield tile90
    yield flip_v(tile90)
    yield flip_h(tile90)
    tile180 = rotate(tile90)
    yield tile180
    yield flip_v(tile180)
    yield flip_h(tile180)
    tile270 = rotate(tile180)
    yield tile270
    yield flip_v(tile270)
    yield flip_h(tile270)


# @cache
# def left_edge(tile):
#     return frozenset(y for x, y in tile if x == 0)
#
#
# @cache
# def right_edge(tile):
#     return frozenset(y for x, y in tile if x == SQUARE_SIZE - 1)
#
#
# @cache
# def top_edge(tile):
#     return frozenset(x for x, y in tile if y == 0)
#
#
# @cache
# def bottom_edge(tile):
#     return frozenset(x for x, y in tile if y == SQUARE_SIZE - 1)
#
#
# def is_neighbour_left(tile, neighbour):
#     return left_edge(tile) == right_edge(neighbour)
#
#
# def is_neighbour_right(tile, neighbour):
#     return right_edge(tile) == left_edge(neighbour)
#
#
# def is_neighbour_up(tile, neighbour):
#     return top_edge(tile) == bottom_edge(neighbour)
#
#
# def is_neighbour_down(tile, neighbour):
#     return bottom_edge(tile) == top_edge(neighbour)
#
#
# def has_neighbour(tile_id, tile, direction_check):
#     for potential_id, potential_variants in VARIANTS.items():
#         if tile_id == potential_id:
#             continue
#         for potential_variant in potential_variants:
#             if direction_check(tile, potential_variant):
#                 return True
#     return False
#
#
# def find_top_left_corners():
#     for tile_id in TILES.keys():
#         if all(not has_neighbour(tile_id, variant, is_neighbour_up) and not has_neighbour(tile_id, variant, is_neighbour_left) for variant in VARIANTS[tile_id]):
#             yield tile_id


def edge_codes(tile):
    top = 0
    bottom = 0
    left = 0
    right = 0
    for x in range(SQUARE_SIZE):
        if (x, 0) in tile:
            top |= 1 << x
        if (x, SQUARE_SIZE - 1) in tile:
            bottom |= 1 << x
    for y in range(SQUARE_SIZE):
        if (0, y) in tile:
            left |= 1 << y
        if (SQUARE_SIZE - 1, y) in tile:
            right |= 1 << y
    return frozenset({top, left, bottom, right})


def find_neighbours(tile_edges):
    neighbours = {}
    for tile_id, edges in tile_edges.items():
        neighbours[tile_id] = set()
        for neighbour_tile, neighbour_edges in tile_edges.items():
            if tile_id == neighbour_tile:
                continue
            if edges & neighbour_edges:
                neighbours[tile_id].add(neighbour_tile)
    return neighbours


with open("input.txt") as input_file:
    TILES = parse_tiles(input_file)
TILE_EDGES = {tile_id: frozenset(chain.from_iterable(edge_codes(variant) for variant in variants(tile))) for tile_id, tile in TILES.items()}

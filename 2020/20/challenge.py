#!/usr/bin/env python3

from collections import namedtuple
from functools import cache
from itertools import chain
from math import prod

SQUARE_SIZE = 10
EdgeCodes = namedtuple("EdgeCodes", "top right bottom left")
MONSTER = {
    (x, y)
    for y, line in enumerate(
"""
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".strip("\n").splitlines()
    )
    for x, c in enumerate(line)
    if c == "#"
}


def parse_tiles(input_file):
    tiles = {}
    this_tile = set()
    for line in input_file.readlines():
        if line.startswith("Tile"):
            if this_tile:
                tiles[this_tile_id] = frozenset(this_tile)
            this_tile_id = int(line.strip()[5:].strip(":"))
            this_tile = set()
            y = 0
            continue
        for x, c in enumerate(line.strip()):
            if c == "#":
                this_tile.add((x, y))
        y += 1
    tiles[this_tile_id] = frozenset(this_tile)
    return tiles


def rotate(tile, square_size):
    return frozenset((square_size - 1 - y, x) for x, y in tile)


def flip_v(tile, square_size):
    return frozenset((x, square_size - 1 - y) for x, y in tile)


def flip_h(tile, square_size):
    return frozenset((square_size - 1 - x, y) for x, y in tile)


def all_variants(tile, square_size=SQUARE_SIZE):
    tilev = flip_v(tile, square_size)
    tileh = flip_h(tile, square_size)
    tile90 = rotate(tile, square_size)
    tile90v = flip_v(tile90, square_size)
    tile90h = flip_h(tile90, square_size)
    tile180 = rotate(tile90, square_size)
    tile180v = flip_v(tile180, square_size)
    tile180h = flip_h(tile180, square_size)
    tile270 = rotate(tile180, square_size)
    tile270v = flip_v(tile270, square_size)
    tile270h = flip_h(tile270, square_size)
    yield tile, edges(tile)
    yield tilev, edges(tilev)
    yield tileh, edges(tileh)
    yield tile90, edges(tile90)
    yield tile90v, edges(tile90v)
    yield tile90h, edges(tile90h)
    yield tile180, edges(tile180)
    yield tile180v, edges(tile180v)
    yield tile180h, edges(tile180h)
    yield tile270, edges(tile270)
    yield tile270v, edges(tile270v)
    yield tile270h, edges(tile270h)


@cache
def edges(tile):
    top = 0
    right = 0
    bottom = 0
    left = 0
    for xy in range(SQUARE_SIZE):
        if (xy, 0) in tile:
            top |= 1 << xy
        if (xy, SQUARE_SIZE - 1) in tile:
            bottom |= 1 << xy
        if (0, xy) in tile:
            left |= 1 << xy
        if (SQUARE_SIZE - 1, xy) in tile:
            right |= 1 << xy
    return EdgeCodes(top, right, bottom, left)


def neighbours(tile_id, all_edges):
    return {other_id for other_id, other_edges in all_edges.items()
            if tile_id != other_id and len(all_edges[tile_id] & other_edges) > 0}


def find_horizontal_neighbour(right_edge_to_match, potential_tiles):
    for potential_tile_id, potential_variants in potential_tiles.items():
        for variant, edge in potential_variants:
            left_edge_to_match = edge.left
            if right_edge_to_match == left_edge_to_match:
                return potential_tile_id, variant
    raise StopIteration("no neighbour here")


def find_vertical_neighbour(bottom_edge_to_match, potential_tiles):
    for potential_tile_id, potential_variants in potential_tiles.items():
        for variant, edge in potential_variants:
            top_edge_to_match = edge.top
            if bottom_edge_to_match == top_edge_to_match:
                return potential_tile_id, variant
    raise StopIteration("no neighbour here")


def find_order(tile_variants):
    for maybe_top_left_corner_id in (tile_id for tile_id in TILES.keys() if len(neighbours(tile_id, EDGES)) == 2):
        for maybe_top_left_corner, _ in tile_variants[maybe_top_left_corner_id]:
            try:
                to_be_placed = set(tile_variants.keys())
                to_be_placed.remove(maybe_top_left_corner_id)
                order = [(maybe_top_left_corner_id, maybe_top_left_corner)]
                for i in range(1, len(tile_variants)):
                    y, x = divmod(i, GRID_SIZE)
                    if x == 0:
                        bottom_edge_to_match = edges(order[(y - 1) * GRID_SIZE][1]).bottom
                        neighbour_id, neighbour_variant = find_vertical_neighbour(bottom_edge_to_match, {tile_id: tile_variants[tile_id] for tile_id in to_be_placed})
                        order.append((neighbour_id, neighbour_variant))
                        to_be_placed.remove(neighbour_id)
                    else:
                        right_edge_to_match = edges(order[i-1][1]).right
                        neighbour_id, neighbour_variant = find_horizontal_neighbour(right_edge_to_match, {tile_id: tile_variants[tile_id] for tile_id in to_be_placed})
                        order.append((neighbour_id, neighbour_variant))
                        to_be_placed.remove(neighbour_id)
                return order
            except StopIteration:
                continue


def strip_borders(tile):
    return {(x - 1, y - 1) for x, y in tile if 0 < x < SQUARE_SIZE - 1 and 0 < y < SQUARE_SIZE - 1}


def stitch_image(order):
    borderless_square_size = SQUARE_SIZE - 2
    image = set()
    for i, (_, tile) in enumerate(order):
        square_y, square_x = divmod(i, GRID_SIZE)
        for tile_x, tile_y in strip_borders(tile):
            image.add((borderless_square_size * square_x + tile_x, borderless_square_size * square_y + tile_y))
    return frozenset(image)


def matches(origin_x, origin_y, fragment, image):
    return all((origin_x + x, origin_y + y) in image for x, y in fragment)


def has_monsters(fragment, image):
    max_x = max(x for x, y in image)
    max_y = max(y for x, y in image)
    return sum(1 for x in range(max_x) for y in range(max_y) if matches(x, y, fragment, image)) > 0


def remove_monsters(fragment, image):
    cleaned_image = set(image)
    max_x = max(x for x, y in image)
    max_y = max(y for x, y in image)
    for origin_x, origin_y in ((x, y) for x in range(max_x) for y in range(max_y) if matches(x, y, fragment, image)):
        cleaned_image -= {(origin_x + monster_x, origin_y + monster_y) for monster_x, monster_y in fragment}
    return cleaned_image


with open("input.txt") as input_file:
    TILES = parse_tiles(input_file)
GRID_SIZE = int(len(TILES) ** 0.5)
VARIANTS = {tile_id: list(all_variants(tile)) for tile_id, tile in TILES.items()}
EDGES = {tile_id: frozenset(chain.from_iterable(edges for tile, edges in variants)) for tile_id, variants in VARIANTS.items()}


print(f"Part One: {prod(tile_id for tile_id in TILES.keys() if len(neighbours(tile_id, EDGES)) == 2)}")
IMAGE_VARIANTS = [v for v, e in all_variants(stitch_image(find_order(VARIANTS)), square_size=GRID_SIZE*(SQUARE_SIZE-2))]
CORRECT_IMAGE = next(variant for variant in IMAGE_VARIANTS if has_monsters(MONSTER, variant))
print(f"Part Two: {len(remove_monsters(MONSTER, CORRECT_IMAGE))}")

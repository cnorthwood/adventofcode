#!/usr/bin/env -S python3 -S
import re

A_COST = 3
B_COST = 1


def load_input(input_filename):
    with open(input_filename) as input_file:
        for line in input_file:
            yielded = False
            if not line.strip():
                yield adx, ady, bdx, bdy, gx, gy
                yielded = True
                continue
            x, y = list(map(int, re.findall(r'\d+', line)))
            if line.startswith("Button A"):
                adx = x
                ady = y
            if line.startswith("Button B"):
                bdx = x
                bdy = y
            if line.startswith("Prize"):
                gx = x
                gy = y
        if not yielded:
            yield adx, ady, bdx, bdy, gx, gy


def solve_presses(game):
    # apply Cramer's rule, explained in https://www.reddit.com/r/adventofcode/comments/1hd7irq/comment/m1xtxxc/
    adx, ady, bdx, bdy, gx, gy = game
    return (gx * bdy - gy * bdx) / (adx * bdy - ady * bdx), (gy * adx - gx * ady) / (adx * bdy - ady * bdx)

def is_solvable(presses):
    return all(p.is_integer() for p in presses)


def cost(game):
    presses = solve_presses(game)
    if not is_solvable(presses):
        return 0

    pa, pb = presses
    return pa * A_COST + pb * B_COST


def part2_game(game):
    adx, ady, bdx, bdy, gx, gy = game
    return adx, ady, bdx, bdy, gx + 10000000000000, gy + 10000000000000


assert(solve_presses((94, 34, 22, 67, 8400, 5400)) == (80, 40))
assert(not is_solvable(solve_presses((26, 66, 67, 21, 12748, 12176))))

GAMES = list(load_input("input.txt"))
print(f"Part One: {int(sum(map(cost, GAMES)))}")
print(f"Part Two: {int(sum(map(cost, map(part2_game, GAMES))))}")

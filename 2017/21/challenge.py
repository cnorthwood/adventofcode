#!/usr/bin/env pypy3

START = (
    (False, True, False),
    (False, False, True),
    (True, True, True),
)


def rotate(pattern):
    if len(pattern) == 2:
        return (
            (pattern[1][0], pattern[0][0]),
            (pattern[1][1], pattern[0][1]),
        )
    elif len(pattern) == 3:
        return (
            (pattern[2][0], pattern[1][0], pattern[0][0]),
            (pattern[2][1], pattern[1][1], pattern[0][1]),
            (pattern[2][2], pattern[1][2], pattern[0][2]),
        )


def flip_h(pattern):
    return tuple(tuple(reversed(row)) for row in pattern)


def flip_v(pattern):
    return tuple(reversed(pattern))


def generate_permutations(pattern):
    return {
        pattern,
        rotate(pattern),
        rotate(rotate(pattern)),
        rotate(rotate(rotate(pattern))),
        flip_h(pattern),
        rotate(flip_h(pattern)),
        rotate(rotate(flip_h(pattern))),
        rotate(rotate(rotate(flip_h(pattern)))),
        flip_v(pattern),
        rotate(flip_v(pattern)),
        rotate(rotate(flip_v(pattern))),
        rotate(rotate(rotate(flip_v(pattern)))),
    }


def parse_rules(input):
    for line in input.splitlines():
        before, after = line.split(' => ')
        before = tuple(tuple([True if c == '#' else False for c in row]) for row in before.split('/'))
        after = tuple(tuple([True if c == '#' else False for c in row]) for row in after.split('/'))
        yield generate_permutations(before), after


assert rotate(((0, 1), (2, 3))) == ((2, 0), (3, 1))
assert rotate(((0, 1, 2), (3, 4, 5), (6, 7, 8))) == ((6, 3, 0), (7, 4, 1), (8, 5, 2))
assert flip_h(((0, 1), (2, 3))) == ((1, 0), (3, 2))
assert flip_v(((0, 1), (2, 3))) == ((2, 3), (0, 1))


def print_grid(grid):
    for row in grid:
        for c in row:
            print('#' if c else '.', end='')
        print()


def divide_row(row):
    if len(row) % 2 == 0:
        for i in range(len(row[0]), step=2):
            yield (
                (row[0][i], row[0][i+1]),
                (row[1][i], row[1][i+1]),
            )
    elif len(row) % 3 == 0:
        for i in range(len(row[0]), step=3):
            yield (
                (row[0][i], row[0][i+1], row[0][i+2]),
                (row[1][i], row[1][i+1], row[1][i+2]),
                (row[2][i], row[2][i+1], row[2][i+2]),
            )


def divide(grid):
    if len(grid) % 2 == 0:
        for i in range(len(grid), step=2):
            yield divide_row(grid[i:i+2])
    elif len(grid) % 3 == 0:
        for i in range(len(grid), step=3):
            yield divide_row(grid[i:i+3])


def apply(grid, rules):
    new_grid = ()
    for row in divide(grid):
        new_row = None
        for cell in row:
            for patterns, after in rules:
                if cell in patterns:
                    if new_row is None:
                        new_row = [() for _ in range(len(after))]
                    for i, pattern_row in enumerate(after):
                        new_row[i] += pattern_row
                    break
            else:
                raise Exception('failed to find a match')
        new_grid += tuple(new_row)
    return new_grid


def part1(input, iterations):
    rules = list(parse_rules(input))
    grid = START
    for _ in range(iterations):
        grid = apply(grid, rules)
        # print('Iteration {}'.format(_))
        # print_grid(grid)
    return sum(sum(row) for row in grid)


TEST_RULES = """
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
""".strip()

assert part1(TEST_RULES, 2) == 12

with open('input.txt') as input_file:
    INPUT = input_file.read().strip()

print("Part One:", part1(INPUT, 5))
print("Part Two:", part1(INPUT, 18))

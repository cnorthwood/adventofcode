#!/usr/bin/env python3 -S

with open("input.txt") as input_file:
    GRID = list(line.strip() for line in input_file)

MAX_Y = len(GRID) - 1
MAX_X = max(len(line) for line in GRID) - 1


def safe_check_char(x, y, expected):
    if x < 0 or x > MAX_X or y < 0 or y > MAX_Y:
        return False

    return GRID[y][x] == expected

def xmas_check_up_left(x, y):
    return safe_check_char(x, y, "X") \
        and safe_check_char(x - 1, y - 1, "M") \
        and safe_check_char(x - 2, y - 2, "A") \
        and safe_check_char(x - 3, y - 3, "S")

def xmas_check_up_right(x, y):
    return safe_check_char(x, y, "X") \
        and safe_check_char(x + 1, y - 1, "M") \
        and safe_check_char(x + 2, y - 2, "A") \
        and safe_check_char(x + 3, y - 3, "S")

def xmas_check_up(x, y):
    return safe_check_char(x, y, "X") \
        and safe_check_char(x, y - 1, "M") \
        and safe_check_char(x, y - 2, "A") \
        and safe_check_char(x, y - 3, "S")

def xmas_check_left(x, y):
    return safe_check_char(x, y, "X") \
        and safe_check_char(x - 1, y, "M") \
        and safe_check_char(x - 2, y, "A") \
        and safe_check_char(x - 3, y, "S")

def xmas_check_right(x, y):
    return safe_check_char(x, y, "X") \
        and safe_check_char(x + 1, y, "M") \
        and safe_check_char(x + 2, y, "A") \
        and safe_check_char(x + 3, y, "S")

def xmas_check_down_left(x, y):
    return safe_check_char(x, y, "X") \
        and safe_check_char(x - 1, y + 1, "M") \
        and safe_check_char(x - 2, y + 2, "A") \
        and safe_check_char(x - 3, y + 3, "S")

def xmas_check_down_right(x, y):
    return safe_check_char(x, y, "X") \
        and safe_check_char(x + 1, y + 1, "M") \
        and safe_check_char(x + 2, y + 2, "A") \
        and safe_check_char(x + 3, y + 3, "S")

def xmas_check_down(x, y):
    return safe_check_char(x, y, "X") \
        and safe_check_char(x, y + 1, "M") \
        and safe_check_char(x, y + 2, "A") \
        and safe_check_char(x, y + 3, "S")

def num_xmas(x, y):
    check_funcs = [xmas_check_up, xmas_check_up_left, xmas_check_up_right, xmas_check_left, xmas_check_right, xmas_check_down, xmas_check_down_left, xmas_check_down_right]
    return sum(1 for f in check_funcs if f(x, y))

def mas_check_down(x, y):
    return (
            safe_check_char(x - 1, y - 1, "M") and safe_check_char(x + 1, y + 1, "S")
        ) or (
            safe_check_char(x - 1, y - 1, "S") and safe_check_char(x + 1, y + 1, "M")
        )

def mas_check_up(x, y):
    return (
            safe_check_char(x - 1, y + 1, "M") and safe_check_char(x + 1, y - 1, "S")
        ) or (
            safe_check_char(x - 1, y + 1, "S") and safe_check_char(x + 1, y - 1, "M")
        )

def num_x_mas(x, y):
    return 1 if safe_check_char(x, y, "A") and mas_check_down(x, y) and mas_check_up(x, y) else 0


print(f"Part One: {sum(num_xmas(x, y) for x in range(MAX_X + 1) for y in range(MAX_Y + 1))}")
print(f"Part Two: {sum(num_x_mas(x, y) for x in range(MAX_X + 1) for y in range(MAX_Y + 1))}")

from itertools import chain

import re

HEIGHT = 6
WIDTH = 50

SCREEN = [[False for x in range(WIDTH)] for y in range(HEIGHT)]


def print_screen():
    for y in range(HEIGHT):
        print ''.join('#' if SCREEN[y][x] else ' ' for x in range(WIDTH))
    print


def rect(a, b):
    for x in range(int(a)):
        for y in range(int(b)):
            SCREEN[y][x] = True


def rotate_row(a, b):
    a = int(a)
    b = int(b)
    SCREEN[a] = [SCREEN[a][(x - b) % WIDTH] for x in range(WIDTH)]


def rotate_column(a, b):
    a = int(a)
    b = int(b)
    new_col = [False] * HEIGHT
    for y in range(HEIGHT):
        new_col[(y + b) % HEIGHT] = SCREEN[y][a]
    for y in range(HEIGHT):
        SCREEN[y][a] = new_col[y]

RECT_PARSER = re.compile(r'^rect (?P<a>\d+)x(?P<b>\d+)$')
ROTATE_ROW_PARSER = re.compile(r'^rotate row y=(?P<a>\d+) by (?P<b>\d+)$')
ROTATE_COL_PARSER = re.compile(r'^rotate column x=(?P<a>\d+) by (?P<b>\d+)$')


def parse(line):
    rect_inst = RECT_PARSER.match(line)
    if rect_inst:
        return rect(**rect_inst.groupdict())

    rotate_row_match = ROTATE_ROW_PARSER.match(line)
    if rotate_row_match:
        return rotate_row(**rotate_row_match.groupdict())

    rotate_column_match = ROTATE_COL_PARSER.match(line)
    if rotate_column_match:
        return rotate_column(**rotate_column_match.groupdict())

# parse('rect 3x2')
# print_screen()
#
# parse('rotate column x=1 by 1')
# print_screen()
#
# parse('rotate row y=0 by 4')
# print_screen()
#
# parse('rotate column x=1 by 1')
# print_screen()

with open('input.txt') as input:
    for line in input:
        parse(line)

print "Part 1:", sum(chain(*SCREEN))
print_screen()

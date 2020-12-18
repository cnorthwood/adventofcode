#!/usr/bin/env python3

def parse_line(line):
    parsed = []
    i = 0
    while i < len(line):
        c = line[i]
        if c.isspace():
            i += 1
            continue
        elif c.isdigit():
            i += 1
            parsed.append(int(c))
        elif c in "+*":
            i += 1
            parsed.append(c)
        elif c == "(":
            consumed, subtree = parse_line(line[i+1:])
            parsed.append(subtree)
            i += consumed + 1
        elif c == ")":
            return i + 1, parsed
        else:
            raise ValueError(c)
    assert i == len(line)
    return i, parsed


def reduce_ltr(line):
    while len(line) > 1:
        left, op, right = line[:3]
        if isinstance(left, list):
            left = reduce_ltr(left)
        if isinstance(right, list):
            right = reduce_ltr(right)
        if op == "+":
            result = left + right
        if op == "*":
            result = left * right
        line = [result] + line[3:]
    if isinstance(line[0], list):
        return reduce_ltr(line[0])
    return line[0]


def reduce_add_first(line):
    while len(line) > 2:
        plus_found = False
        for i, op in enumerate(line):
            if op == "+":
                left, right = line[i-1], line[i+1]
                if isinstance(left, list):
                    left = reduce_add_first(left)
                if isinstance(right, list):
                    right = reduce_add_first(right)
                result = left + right
                line = line[:i-1] + [result] + line[i+2:]
                plus_found = True
                break
        if plus_found:
            continue
        for i, op in enumerate(line):
            if op == "*":
                left, right = line[i-1], line[i+1]
                if isinstance(left, list):
                    left = reduce_add_first(left)
                if isinstance(right, list):
                    right = reduce_add_first(right)
                result = left * right
                line = line[:i-1] + [result] + line[i+2:]
                break
    if isinstance(line[0], list):
        return reduce_add_first(line[0])
    return line[0]


assert reduce_ltr(parse_line("2 * 3 + (4 * 5)")[1]) == 26
assert reduce_ltr(parse_line("5 + (8 * 3 + 9 + 3 * 4 * 3)")[1]) == 437
assert reduce_ltr(parse_line("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")[1]) == 12240
assert reduce_ltr(parse_line("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")[1]) == 13632

assert reduce_add_first(parse_line("2 * 3 + (4 * 5)")[1]) == 46
assert reduce_add_first(parse_line("5 + (8 * 3 + 9 + 3 * 4 * 3)")[1]) == 1445
assert reduce_add_first(parse_line("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")[1]) == 669060
assert reduce_add_first(parse_line("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")[1]) == 23340


with open("input.txt") as input_file:
    INPUT = [parse_line(line.strip())[1] for line in input_file.readlines()]
print(f"Part One: {sum(reduce_ltr(line) for line in INPUT)}")
print(f"Part Two: {sum(reduce_add_first(line) for line in INPUT)}")

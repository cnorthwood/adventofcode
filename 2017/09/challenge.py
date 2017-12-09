#!/usr/bin/env python3


def parse_group(input, start_score):
    score = start_score
    in_garbage = False
    while input:
        c, input = input[0], input[1:]
        if c == '!':
            input = input[1:]
            continue

        if in_garbage:
            if c == '>':
                in_garbage = False
                continue
            else:
                continue

        if c == '{':
            nested_score, input = parse_group(input, start_score + 1)
            score += nested_score
            continue
        elif c == ',':
            continue
        elif c == '}':
            break
        elif c == '<':
            in_garbage = True
            continue
        raise Exception('unrecognised character {}'.format(c))

    return score, input


assert parse_group('{}', 0) == (1, '')
assert parse_group('{{{}}}', 0) == (6, '')
assert parse_group('{{},{}}', 0) == (5, '')
assert parse_group('{{{},{},{{}}}}', 0) == (16, '')
assert parse_group('{<a>,<a>,<a>,<a>}', 0) == (1, '')
assert parse_group('{{<ab>},{<ab>},{<ab>},{<ab>}}', 0) == (9, '')
assert parse_group('{{<!!>},{<!!>},{<!!>},{<!!>}}', 0) == (9, '')
assert parse_group('{{<a!>},{<a!>},{<a!>},{<ab>}}', 0) == (3, '')

with open('input.txt') as input:
    INPUT = input.read().strip()

print("Part One:", parse_group(INPUT, 0)[0])


def count_garbage(input):
    garbage_chars = 0
    in_garbage = False
    while input:
        c, input = input[0], input[1:]
        if c == '!':
            input = input[1:]
            continue

        if in_garbage:
            if c == '>':
                in_garbage = False
                continue
            else:
                garbage_chars += 1
                continue

        elif c == '<':
            in_garbage = True

    return garbage_chars


assert count_garbage('<>') == 0
assert count_garbage('<random characters>') == 17
assert count_garbage('<<<<>') == 3
assert count_garbage('<{!>}>') == 2
assert count_garbage('<!!>') == 0
assert count_garbage('<!!!>>') == 0
assert count_garbage('<{o"i!a,<{i<a>') == 10

print("Part Two:", count_garbage(INPUT))

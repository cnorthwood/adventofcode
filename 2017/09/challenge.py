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

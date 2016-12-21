from collections import deque
import re


SWAP_POS_RE = re.compile(r'swap position (?P<x>\d+) with position (?P<y>\d+)')
def swap_pos(password, x, y):
    x, y = sorted([int(x), int(y)])
    return password[:x] + password[y] + password[x+1:y] + password[x] + password[y+1:]


SWAP_LETTER_RE = re.compile(r'swap letter (?P<x>\w+) with letter (?P<y>\w+)')
def swap_letter(password, x, y):
    def swapper(c):
        if c == x:
            return y
        elif c == y:
            return x
        else:
            return c
    return ''.join(swapper(c) for c in password)



ROTATE_RE = re.compile(r'rotate (?P<direction>left|right) (?P<x>\d+) steps?')
def rotate(password, direction, x):
    password = deque(password)
    x = int(x)
    if direction == 'left':
        x = -x
    password.rotate(x)
    return ''.join(password)


ROTATE_POSITION_RE = re.compile(r'rotate based on position of letter (?P<x>\w+)')
def rotate_position(password, x):
    i = password.index(x)
    password = deque(password)
    if i >= 4:
        i += 1
    i += 1
    password.rotate(i)
    return ''.join(password)


REVERSE_POS_RE = re.compile(r'reverse positions (?P<x>\d+) through (?P<y>\d+)')
def reverse_pos(password, x, y):
    x = int(x)
    y = int(y)
    return password[:x] + ''.join(reversed(password[x:y+1])) + password[y+1:]


MOVE_RE = re.compile(r'move position (?P<x>\d+) to position (?P<y>\d+)')
def move(password, x, y):
    x = int(x)
    y = int(y)
    new_password = password[:x] + password[x+1:]
    new_password = new_password[:y] + password[x] + new_password[y:]
    return new_password


assert swap_pos('abcde', '4', '0') == 'ebcda'
assert swap_letter('ebcda', 'd', 'b') == 'edcba'
assert reverse_pos('edcba', '0', '4') == 'abcde'
assert rotate('abcde', 'left', '1') == 'bcdea'
assert move('bcdea', '1', '4') == 'bdeac'
assert move('bdeac', '3', '0') == 'abdec'
assert rotate_position('abdec', 'b') == 'ecabd'
assert rotate_position('ecabd', 'd') == 'decab'

with open('input.txt') as input:
    password = 'abcdefgh'
    for line in input:
        swap_pos_match = SWAP_POS_RE.match(line)
        if swap_pos_match:
            password = swap_pos(password, **swap_pos_match.groupdict())
            continue

        swap_letter_match = SWAP_LETTER_RE.match(line)
        if swap_letter_match:
            password = swap_letter(password, **swap_letter_match.groupdict())
            continue

        rotate_match = ROTATE_RE.match(line)
        if rotate_match:
            password = rotate(password, **rotate_match.groupdict())
            continue

        rotate_position_match = ROTATE_POSITION_RE.match(line)
        if rotate_position_match:
            password = rotate_position(password, **rotate_position_match.groupdict())
            continue

        reverse_pos_match = REVERSE_POS_RE.match(line)
        if reverse_pos_match:
            password = reverse_pos(password, **reverse_pos_match.groupdict())
            continue

        move_match = MOVE_RE.match(line)
        if move_match:
            password = move(password, **move_match.groupdict())
            continue


print "Part One:", password

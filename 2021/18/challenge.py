#!/usr/bin/env pypy3
import re
from functools import reduce
from itertools import permutations
from math import floor, ceil


def snailfish_apply_explode(number):
    number = number[:]
    level = 0
    for i in range(len(number)):
        if number[i] == "[":
            level += 1
        elif number[i] == "]":
            level -= 1

        if level > 4:
            left = int(number[i+1])
            right = int(number[i+3])
            last_number_i = i
            while last_number_i > 0:
                last_number_i -= 1
                if str.isdigit(number[last_number_i]):
                    number[last_number_i] = str(int(number[last_number_i]) + left)
                    break
            next_number_i = i + 5
            while next_number_i < len(number):
                if str.isdigit(number[next_number_i]):
                    number[next_number_i] = str(int(number[next_number_i]) + right)
                    break
                next_number_i += 1
            return True, number[:i] + ["0"] + number[i+5:]

    return False, number


assert "".join(snailfish_apply_explode(list("[[[[[9,8],1],2],3],4]"))[1]) == "[[[[0,9],2],3],4]"
assert "".join(snailfish_apply_explode(list("[7,[6,[5,[4,[3,2]]]]]"))[1]) == "[7,[6,[5,[7,0]]]]"
assert "".join(snailfish_apply_explode(list("[[6,[5,[4,[3,2]]]],1]"))[1]) == "[[6,[5,[7,0]]],3]"
assert "".join(snailfish_apply_explode(list("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"))[1]) == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
assert "".join(snailfish_apply_explode(list("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"))[1]) == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"


def snailfish_apply_split(number):
    for i, n in enumerate(number):
        if str.isdigit(n) and int(n) >= 10:
            return True, number[:i] + ["[", str(int(floor(int(n) / 2.0))), ",", str(int(ceil(int(n) / 2.0))), "]"] + number[i+1:]
    return False, number


assert "".join(snailfish_apply_split(["10"])[1]) == "[5,5]"
assert "".join(snailfish_apply_split(["11"])[1]) == "[5,6]"
assert "".join(snailfish_apply_split(["12"])[1]) == "[6,6]"


def snailfish_reduce(number):
    number = list(number)
    while True:
        exploded, number = snailfish_apply_explode(number)
        if exploded:
            continue
        split, number = snailfish_apply_split(number)
        if not split:
            return ''.join(number)


def snailfish_add(a, b):
    return snailfish_reduce(f"[{a},{b}]")


assert snailfish_add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


def snailfish_magitude(number):
    subs = 1
    while subs > 0:
        number, subs = re.subn(r"\[(\d+),(\d+)]", lambda match: str(3 * int(match.group(1)) + 2 * int(match.group(2))), number)
    return int(number)

assert snailfish_magitude("[[1,2],[[3,4],5]]") == 143
assert snailfish_magitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
assert snailfish_magitude("[[[[1,1],[2,2]],[3,3]],[4,4]]") == 445
assert snailfish_magitude("[[[[3,0],[5,3]],[4,4]],[5,5]]") == 791
assert snailfish_magitude("[[[[5,0],[7,4]],[5,5]],[6,6]]") == 1137
assert snailfish_magitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]") == 3488


with open("input.txt") as input_file:
    INPUT = [line.strip() for line in input_file]
print(f"Part One: {snailfish_magitude(reduce(snailfish_add, INPUT))}")
print(f"Part Two: {max(snailfish_magitude(snailfish_add(a, b)) for a, b in permutations(INPUT, 2))}")

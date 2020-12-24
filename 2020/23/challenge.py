#!/usr/bin/env pypy3

with open("input.txt") as input_file:
    INPUT = [int(p) for p in input_file.read().strip()]


def convert_to_pointers(cups):
    pointers = {cup: next_cup for cup, next_cup in zip(cups, cups[1:])}
    pointers[cups[-1]] = cups[0]
    return pointers


def step(current_cup, cups):
    selected_cups = [cups[current_cup]]
    selected_cups.append(cups[selected_cups[-1]])
    selected_cups.append(cups[selected_cups[-1]])
    cups[current_cup] = cups[selected_cups[-1]]
    next_label = current_cup - 1
    while next_label in selected_cups or next_label < 1:
        next_label -= 1
        if next_label < 1:
            next_label = max(cups)
    cups[selected_cups[-1]] = cups[next_label]
    cups[next_label] = selected_cups[0]
    return cups[current_cup]


def part_one_answer(cups):
    current_cup = cups[1]
    while current_cup != 1:
        yield current_cup
        current_cup = cups[current_cup]


part_one_cups = convert_to_pointers(INPUT)
current_cup = INPUT[0]
for _ in range(100):
    current_cup = step(current_cup, part_one_cups)
print(f"Part One: {''.join(str(n) for n in part_one_answer(part_one_cups))}")
part_two_cups = convert_to_pointers(INPUT + list(range(max(INPUT) + 1, 1000001)))
assert len(part_two_cups) == 1000000
current_cup = INPUT[0]
for _ in range(10000000):
    if _ % 100000 == 0:
        print(_)
    current_cup = step(current_cup, part_two_cups)
print(f"Part Two: {part_two_cups[1] * part_two_cups[part_two_cups[1]]}")
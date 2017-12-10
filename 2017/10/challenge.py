#!/usr/bin/env python3


def rotate(start, length, data):
    slots = [None] * len(data)
    for i in range(length):
        slots[(start + i) % len(data)] = data[(start + length - i - 1) % len(data)]
    for i, slot in enumerate(slots):
        if slot is None:
            slots[i] = data[i]
    return slots


assert rotate(0, 3, [0, 1, 2, 3, 4]) == [2, 1, 0, 3, 4]
assert rotate(3, 4, [2, 1, 0, 3, 4]) == [4, 3, 0, 1, 2]


INPUT = map(int, "106,118,236,1,130,0,235,254,59,205,2,87,129,25,255,118".split(','))

current_location = 0
data = list(range(256))
for skip, item in enumerate(INPUT):
    data = rotate(current_location, item, data)
    current_location += skip + item

print("Part One:", data[0] * data[1])

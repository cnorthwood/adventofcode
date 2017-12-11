#!/usr/bin/env python3

def distance(steps):
    target_x, target_y = 0, 0
    for step in steps:
        if step == 'ne':
            target_x += 1
            target_y += 1 if target_x % 2 == 1 else 0
        elif step == 'nw':
            target_x -= 1
            target_y += 1 if target_x % 2 == 1 else 0
        elif step == 'se':
            target_x += 1
            target_y -= 1 if target_x % 2 == 0 else 0
        elif step == 'sw':
            target_x -= 1
            target_y -= 1 if target_x % 2 == 0 else 0
        elif step == 'n':
            target_y += 1
        elif step == 's':
            target_y -= 1
        else:
            raise Exception(step)

    current_x, current_y = 0, 0
    steps = 0
    while (current_x, current_y) != (target_x, target_y):
        steps += 1
        if target_x == current_x:
            if current_y < target_y:
                # move north
                current_y += 1
                # print('n', current_x, current_y)
            else:
                # move south
                current_y -= 1
                # print('s', current_x, current_y)
        elif target_x > current_x:
            if current_y < target_y or (current_y == target_y and current_x % 2 == 0):
                # move ne
                current_x += 1
                current_y += 1 if current_x % 2 == 1 else 0
                # print('ne', current_x, current_y)
            else:
                # move se
                current_x += 1
                current_y -= 1 if current_x % 2 == 0 else 0
                # print('se', current_x, current_y)
        elif target_x < current_x:
            if current_y < target_y or (current_y == target_y and current_x % 2 == 0):
                # move nw
                current_x -= 1
                current_y += 1 if current_x % 2 == 1 else 0
                # print('nw', current_x, current_y)
            else:
                # move sw
                current_x -= 1
                current_y -= 1 if current_x % 2 == 0 else 0
                # print('sw', current_x, current_y)
        else:
            raise Exception('stuck')
    return steps


assert distance(['ne', 'ne', 'ne']) == 3
assert distance(['ne', 'ne', 'sw', 'sw']) == 0
assert distance(['ne', 'ne', 's', 's']) == 2
assert distance(['se', 'sw', 'se', 'sw', 'sw']) == 3

with open('input.txt') as input:
    INPUT = input.read().strip().split(',')
print("Part One:", distance(INPUT))
print("Part Two:", max(distance(INPUT[:i]) for i in range(len(INPUT))))

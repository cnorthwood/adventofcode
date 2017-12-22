#!/usr/bin/env pypy3

RIGHTS = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N',
}

LEFTS = {
    'N': 'W',
    'E': 'N',
    'S': 'E',
    'W': 'S',
}

REVERSES = {
    'N': 'S',
    'E': 'W',
    'S': 'N',
    'W': 'E',
}


def parse(grid):
    infected = set()
    for y, row in enumerate(reversed(grid.splitlines())):
        for x, c in enumerate(row):
            if c == '#':
                infected.add((x, y))
    return infected, (x // 2, y // 2)


def tick(pos, direction, infected):
    if pos in infected:
        direction = RIGHTS[direction]
        infected.remove(pos)
        did_infect = False
    else:
        direction = LEFTS[direction]
        infected.add(pos)
        did_infect = True
    
    x, y = pos
    if direction == 'N':
        y += 1
    elif direction == 'S':
        y -= 1
    elif direction == 'E':
        x += 1
    elif direction == 'W':
        x -= 1
    
    return (x, y), direction, did_infect


def main(start, infected, ticks=10000):
    pos, direction = start, 'N'
    infections = 0
    for _ in range(ticks):
        pos, direction, did_infect = tick(pos, direction, infected)
        if did_infect:
            infections += 1
    return infections


def tick2(pos, direction, infected, weakened, flagged):
    did_infect = False
    if pos in infected:
        direction = RIGHTS[direction]
        infected.remove(pos)
        flagged.add(pos)
    elif pos in weakened:
        weakened.remove(pos)
        infected.add(pos)
        did_infect = True
    elif pos in flagged:
        direction = REVERSES[direction]
        flagged.remove(pos)
    else:
        direction = LEFTS[direction]
        weakened.add(pos)

    x, y = pos
    if direction == 'N':
        y += 1
    elif direction == 'S':
        y -= 1
    elif direction == 'E':
        x += 1
    elif direction == 'W':
        x -= 1

    return (x, y), direction, did_infect


def main2(start, infected, ticks=10000000):
    pos, direction = start, 'N'
    infections = 0
    weakened = set()
    flagged = set()
    for _ in range(ticks):
        pos, direction, did_infect = tick2(pos, direction, infected, weakened, flagged)
        if did_infect:
            infections += 1
    return infections


assert main((0, 0), {(-1, 0), (1, 1)}, 7) == 5
assert main((0, 0), {(-1, 0), (1, 1)}, 70) == 41
assert main((0, 0), {(-1, 0), (1, 1)}) == 5587
assert main2((0, 0), {(-1, 0), (1, 1)}, 100) == 26
assert main2((0, 0), {(-1, 0), (1, 1)}) == 2511944

with open('input.txt') as input_file:
    INFECTED, START = parse(input_file.read().strip())

print("Part One:", main(START, set(INFECTED)))
print("Part Two:", main2(START, set(INFECTED)))

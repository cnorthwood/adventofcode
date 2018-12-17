#!/usr/bin/env pypy3

from collections import deque
from itertools import count, chain
import sys


def find_path(start, end, blocked_locations):
    seen = set()
    paths = deque([[start]])
    while paths:
        path = paths.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path[1:]
        for next_pos in [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]:
            if next_pos not in seen and next_pos not in blocked_locations:
                seen.add(next_pos)
                paths.append(path + [next_pos])
    return None


def print_grid(grid):
    grid = {unit.pos: unit for unit in grid}
    max_x = max(x for (x, y) in grid.keys())
    max_y = max(y for (x, y) in grid.keys())
    sys.stdout.write('\n')
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in grid:
                if isinstance(grid[x, y], Wall):
                    sys.stdout.write('#')
                elif grid[x, y].alignment == Unit.ELF:
                    sys.stdout.write('E')
                elif grid[x, y].alignment == Unit.GOBLIN:
                    sys.stdout.write('G')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')
    sys.stdout.write('\n')


class GameOver(Exception):
    pass


class UnacceptableDeath(Exception):
    pass


class Wall:
    def __init__(self, x, y):
        self.pos = (x, y)


class Unit:

    ELF = 1
    GOBLIN = 2

    def __init__(self, start_x, start_y, alignment, superpower):
        if superpower:
            self._attack_power = superpower
            self.throw_on_death = True
        else:
            self.throw_on_death = False
            self._attack_power = 3
        self.hp = 200
        self.alignment = alignment
        if self.alignment == self.ELF:
            self._opponent = self.GOBLIN
        if self.alignment == self.GOBLIN:
            self._opponent = self.ELF

        self.pos = (start_x, start_y)

    def open_squares(self, grid):
        return self._get_adjacent() - {unit.pos for unit in grid}

    def turn(self, grid):
        enemies_exist = any(unit.alignment == self._opponent for unit in filter(lambda u: isinstance(u, Unit), grid))
        if not enemies_exist:
            raise GameOver()
        if not self._in_range(grid):
            self._move(grid)
        if self._in_range(grid):
            self._attack(grid)

    def _move(self, grid):
        targets = list(chain(*(list(unit.open_squares(grid)) for unit in self._enemies(grid))))
        blocked_locations = {unit.pos for unit in grid}
        all_paths = sorted(
            filter(lambda p: p is not None, (find_path(self.pos, end, blocked_locations) for end in targets)),
            key=lambda p: len(p)
        )
        all_paths = sorted(
            (path for path in all_paths if path is not None and len(path) == len(all_paths[0])),
            key=lambda path: (path[0][1], path[0][0])
        )
        if all_paths:
            self.pos = all_paths[0][0]

    def _enemies(self, grid):
        return {
            unit for unit in filter(lambda u: isinstance(u, Unit), grid) if unit.alignment == self._opponent
        }

    def _in_range(self, grid):
        return self._get_adjacent() & {unit.pos for unit in self._enemies(grid)}

    def _attack(self, grid):
        targets = self._in_range(grid)
        targets = sorted((unit for unit in filter(lambda u: isinstance(u, Unit), grid) if unit.pos in targets), key=lambda unit: unit.hp)
        target = sorted(
            (target for target in targets if target.hp == targets[0].hp),
            key=lambda unit: (unit.pos[1], unit.pos[0])
        )[0]
        target.hp -= self._attack_power
        if target.hp <= 0:
            if target.throw_on_death:
                raise UnacceptableDeath()
            grid.remove(target)

    def _get_highest_priority(self, positions):
        return min(positions, key=lambda pos: (pos[1], pos[0]))

    def _get_adjacent(self):
        x, y = self.pos
        return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}


def battle_round(grid):
    for unit in sorted(filter(lambda u: isinstance(u, Unit), grid), key=lambda u: (u.pos[1], u.pos[0])):
        if unit in grid:
            unit.turn(grid)


def load_map(filename, super_elf=0):
    with open(filename) as input_file:
        lines = input_file.read().strip().splitlines()
    grid = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                grid.add(Wall(x, y))
            elif c == 'G':
                grid.add(Unit(x, y, Unit.GOBLIN, 0))
            elif c == 'E':
                grid.add(Unit(x, y, Unit.ELF, super_elf))
    return grid


def part_one(filename):
    grid = load_map(filename)
    for n in count():
        try:
            battle_round(grid)
        except GameOver:
            return n * sum(unit.hp for unit in filter(lambda u: isinstance(u, Unit), grid))


# assert(part_one('test.txt') == 27730)
# assert(part_one('test2.txt') == 36334)
# assert(part_one('test3.txt') == 39514)
# assert(part_one('test4.txt') == 27755)
# assert(part_one('test5.txt') == 28944)
# assert(part_one('test6.txt') == 18740)
print("Part One: {}".format(part_one('input.txt')))


def part_two(filename):
    for elf_power in count(3):
        grid = load_map(filename, super_elf=elf_power)
        for n in count():
            try:
                battle_round(grid)
            except UnacceptableDeath:
                break
            except GameOver:
                return n * sum(unit.hp for unit in filter(lambda u: isinstance(u, Unit), grid))


print("Part Two: {}".format(part_two('input.txt')))

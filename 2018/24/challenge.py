#!/usr/bin/env pypy3

import re
from itertools import count

INPUT_RE = re.compile(r'(?P<units>\d+) units each with (?P<hp>\d+) hit points (?P<boosts>.+ )?with an attack that does (?P<damage>\d+) (?P<dtype>.+) damage at initiative (?P<initiative>\d+)')
WEAK_RE = re.compile(r'weak to (?P<weaknesses>[\w, ]+)')
IMMUNE_RE = re.compile(r'immune to (?P<immunities>[\w, ]+)')


class Army:
    IMMUNE = 'Immune'
    INFECTION = 'Infection'

    def __init__(self, alignment, units, hp, dpoints, dtype, initiative, immunities, weaknesses):
        self.alignment = alignment
        self.units = units
        self.hp = hp
        self.dpoints = dpoints
        self.dtype = dtype
        self.initiative = initiative
        self.immunities = immunities
        self.weaknesses = weaknesses

    @classmethod
    def create_from_line(cls, alignment, line):
        match = INPUT_RE.match(line)
        weakness_match = WEAK_RE.search(line)
        immunity_match = IMMUNE_RE.search(line)
        return cls(
            alignment,
            int(match.group('units')),
            int(match.group('hp')),
            int(match.group('damage')),
            match.group('dtype'),
            int(match.group('initiative')),
            immunity_match.group('immunities').split(', ') if immunity_match else [],
            weakness_match.group('weaknesses').split(', ') if weakness_match else [],
        )

    def copy(self):
        return Army(self.alignment,
                    self.units,
                    self.hp,
                    self.dpoints,
                    self.dtype,
                    self.initiative,
                    list(self.immunities),
                    list(self.weaknesses))

    def effective_power(self, defender=None):
        multiplier = 1
        if defender and self.dtype in defender.weaknesses:
            multiplier = 2
        elif defender and self.dtype in defender.immunities:
            multiplier = 0
        return max(0, self.units) * self.dpoints * multiplier

    def attack(self, defender):
        defender.units -= self.effective_power(defender) // defender.hp

    def select_target(self, defenders):
        if defenders:
            target = max(defenders, key=lambda d: (self.effective_power(d), d.effective_power(), d.initiative))
            if self.effective_power(target) > 0:
                return target

    def __str__(self):
        return "{}: {} units each with {} hit points with an attack that does {} {} damage at initiative {} (weak to {}; immune to {})".format(
            self.alignment,
            self.units,
            self.hp,
            self.dpoints,
            self.dtype,
            self.initiative,
            ', '.join(self.weaknesses),
            ', '.join(self.immunities),
        )


def load_input(filename):
    with open(filename) as input_file:
        immune_lines, infection_lines = input_file.read().strip().split('\n\n')
    return [Army.create_from_line(Army.IMMUNE, line) for line in immune_lines.splitlines()[1:]] + [Army.create_from_line(Army.INFECTION, line) for line in infection_lines.splitlines()[1:]]


class ReindeerDeathError(Exception):
    pass


class Stalemate(Exception):
    pass


def assign_targets(armies):
    assignments = {}
    for army in sorted(armies, key=lambda a: (a.units * a.dpoints, a.initiative), reverse=True):
        opponent = Army.IMMUNE if army.alignment == Army.INFECTION else Army.INFECTION
        assignments[army] = army.select_target([a for a in armies if a.alignment == opponent and a not in assignments.values()])
    return assignments


def fight(armies, boost_immune=None):
    armies = [a.copy() for a in armies]
    for army in armies:
        if army.alignment == Army.IMMUNE and boost_immune:
            army.dpoints += boost_immune
    num_units = sum(a.units for a in armies)
    while any(a.alignment == Army.IMMUNE for a in armies) and any(a.alignment == Army.INFECTION for a in armies):
        for attacker, defender in sorted(assign_targets(armies).items(), key=lambda a: a[0].initiative, reverse=True):
            if defender is not None:
                attacker.attack(defender)
                if defender.units <= 0:
                    armies.remove(defender)
        if boost_immune and not any(a.alignment == Army.IMMUNE for a in armies):
            raise ReindeerDeathError()
        next_num_units = sum(a.units for a in armies)
        if num_units == next_num_units:
            raise Stalemate()
        num_units = next_num_units
    return num_units


def find_boost(armies):
    for boost in count(1):
        try:
            return fight(armies, boost)
        except (ReindeerDeathError, Stalemate):
            continue


TEST = load_input('test.txt')
INPUT = load_input('input.txt')

assert(fight(TEST) == 5216)
assert(find_boost(TEST) == 51)
print("Part One: {}".format(fight(INPUT)))
print("Part Two: {}".format(find_boost(INPUT)))

#!/usr/bin/env pypy3

import re
from itertools import count

INPUT_RE = re.compile(r'(?P<units>\d+) units each with (?P<hp>\d+) hit points (?P<boosts>.+ )?with an attack that does (?P<damage>\d+) (?P<dtype>.+) damage at initiative (?P<initiative>\d+)')
WEAK_RE = re.compile(r'weak to (?P<weaknesses>[\w, ]+)')
IMMUNE_RE = re.compile(r'immune to (?P<immunities>[\w, ]+)')


class Army:
    def __init__(self, alignment, units, hp, dpoints, dtype, initiative, immunities, weaknesses):
        self.alignment = alignment
        self.units = units
        self.hp = hp
        self.dpoints = dpoints
        self.dtype = dtype
        self.initiative = initiative
        self.immunities = immunities
        self.weaknesses = weaknesses

    def copy(self):
        return Army(self.alignment,
                    self.units,
                    self.hp,
                    self.dpoints,
                    self.dtype,
                    self.initiative,
                    list(self.immunities),
                    list(self.weaknesses))

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


def build_armies(lines, alignment):
    for line in lines:
        match = INPUT_RE.match(line)
        weakness_match = WEAK_RE.search(line)
        immunity_match = IMMUNE_RE.search(line)
        yield Army(
            alignment,
            int(match.group('units')),
            int(match.group('hp')),
            int(match.group('damage')),
            match.group('dtype'),
            int(match.group('initiative')),
            immunity_match.group('immunities').split(', ') if immunity_match else [],
            weakness_match.group('weaknesses').split(', ') if weakness_match else [],
        )


def load_input(filename):
    with open(filename) as input_file:
        immune_lines, infection_lines = input_file.read().strip().split('\n\n')
    return list(build_armies(immune_lines.splitlines()[1:], 'immune')) + list(build_armies(infection_lines.splitlines()[1:], 'infection'))


def damage(attacker, defender):
    effective_power = attacker.units * attacker.dpoints
    if attacker.dtype in defender.immunities:
        return 0
    elif attacker.dtype in defender.weaknesses:
        return 2 * effective_power
    else:
        return effective_power


def select_target(attacker, defenders):
    if defenders:
        return max(defenders, key=lambda d: (damage(attacker, d), d.units * d.dpoints, d.initiative))
    else:
        return None


def assign_targets(armies):
    assignments = {}
    for army in sorted(armies, key=lambda a: (a.units * a.dpoints, a.initiative), reverse=True):
        opponent = 'immune' if army.alignment == 'infection' else 'infection'
        assignments[army] = select_target(army, [a for a in armies if a.alignment == opponent and a not in assignments.values()])
    return assignments


class ReindeerDeathError(Exception):
    pass


class Stalemate(Exception):
    pass


def fight(armies, boost_immune=None):
    armies = [a.copy() for a in armies]
    for army in armies:
        if army.alignment == 'immune' and boost_immune:
            army.dpoints += boost_immune
    num_units = sum(a.units for a in armies)
    while sum(1 for a in armies if a.alignment == 'immune') > 0 and sum(1 for a in armies if a.alignment == 'infection') > 0:
        for attacker, defender in sorted(assign_targets(armies).items(), key=lambda a: a[0].initiative, reverse=True):
            if attacker.units > 0 and defender is not None:
                damage_done = damage(attacker, defender)
                if damage_done:
                    defender.units -= damage_done // defender.hp
                if defender.units <= 0:
                    armies.remove(defender)
        if boost_immune and sum(1 for a in armies if a.alignment == 'immune') == 0:
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

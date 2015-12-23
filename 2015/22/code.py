from collections import namedtuple
from itertools import count
from random import sample

PLAYER_HP = 50
PLAYER_MANA = 500
BOSS_HP = 71
BOSS_DAMAGE = 10

Spell = namedtuple('Spell', ['name', 'cost'])
Effect = namedtuple('Effect', ['name', 'turns'])

SPELLS = {
    Spell('Magic Missile', 53),
    Spell('Drain', 73),
    Spell('Shield', 113),
    Spell('Poison', 173),
    Spell('Recharge', 229)
}

LOWEST_COST = min(spell.cost for spell in SPELLS)


def apply_effects(stats):
    stats['player_armour'] = 0
    for (effect, turns) in frozenset(stats['effects']):
        stats['effects'].remove((effect, turns))
        if effect == 'Shield': stats['player_armour'] = 7
        if effect == 'Poison': stats['boss_hp'] -= 3
        if effect == 'Recharge': stats['mana'] += 101
        if turns > 1:
            stats['effects'].add(Effect(effect, turns - 1))


def get_spell():
    return sample(SPELLS, 1)[0]


def player_wins():
    stats = {
        'mana_spent': 0,
        'mana': PLAYER_MANA,
        'player_hp': PLAYER_HP,
        'boss_hp': BOSS_HP,
        'effects': set(),
        'player_armour': 0
    }

    while True:

        stats['player_hp'] -= 1
        if stats['player_hp'] <= 0:
            return False, stats['mana_spent'], "player killed by hard mode"

        apply_effects(stats)

        if stats['boss_hp'] <= 0:
            return True, stats['mana_spent'], "boss dies through effects on our turn"

        if stats['mana'] < LOWEST_COST:
            return False, stats['mana_spent'], "out of mana"

        spell, cost = get_spell()
        while cost > stats['mana']:
            spell, cost = get_spell()

        while spell in [effect.name for effect in stats['effects']]:
            # print spell, stats['effects']
            spell, cost = get_spell()

        stats['mana'] -= cost
        stats['mana_spent'] += cost

        if spell == 'Magic Missile': stats['boss_hp'] -= 4
        if spell == 'Drain':
            stats['boss_hp'] -= 2
            stats['player_hp'] += 2
        if spell == 'Shield': stats['effects'].add(Effect('Shield', 6))
        if spell == 'Poison': stats['effects'].add(Effect('Poison', 6))
        if spell == 'Recharge': stats['effects'].add(Effect('Recharge', 5))

        if stats['boss_hp'] <= 0:
            return True, stats['mana_spent'], "boss dies through spell"

        apply_effects(stats)

        if stats['boss_hp'] <= 0:
            return True, stats['mana_spent'], "boss dies through effects on their turn"

        stats['player_hp'] -= max(BOSS_DAMAGE - stats['player_armour'], 1)

        if stats['player_hp'] <= 0:
            return False, stats['mana_spent'], "player killed by boss"

    return False, stats['mana_spent']


winning_costs = set()

for i in count():
    if i % 10000 == 0: print str(i), "rounds, lowest mana cost:", min(winning_costs or [0])
    wins, cost, reason = player_wins()
    if wins:
        winning_costs.add(cost)

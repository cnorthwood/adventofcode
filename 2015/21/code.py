from collections import namedtuple
from itertools import chain, combinations, product, ifilterfalse

Item = namedtuple('Item', ['cost', 'damage', 'armour'])

BOSS_HIT_POINTS = 100
BOSS_DAMAGE = 8
BOSS_ARMOUR = 2

INPUT_WEAPONS = """
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
"""

INPUT_ARMOUR = """
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
"""

INPUT_RINGS = """
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

WEAPONS = set(Item(*map(int, line.split()[1:])) for line in INPUT_WEAPONS.splitlines()[1:])
ARMOUR = set(Item(*map(int, line.split()[1:])) for line in INPUT_ARMOUR.splitlines()[1:])
RINGS = set(Item(*map(int, line.split()[2:])) for line in INPUT_RINGS.splitlines()[1:])


def player_wins(items):
    player_hp = 100
    player_damage = sum(item.damage for item in chain.from_iterable(items))
    player_armour = sum(item.armour for item in chain.from_iterable(items))
    boss_hp = BOSS_HIT_POINTS
    while True:
        boss_hp -= max(player_damage - BOSS_ARMOUR, 1)
        if boss_hp <= 0: return True
        player_hp -= max(BOSS_DAMAGE - player_armour, 1)
        if player_hp <= 0: return False


def cost(items):
    return sum(item.cost for item in chain.from_iterable(items))

print "Part One:", min(map(cost, filter(player_wins, product(combinations(WEAPONS, 1), list(chain.from_iterable(combinations(ARMOUR, n) for n in xrange(2))), list(chain.from_iterable(combinations(RINGS, n) for n in xrange(3)))))))
print "Part Two:", max(map(cost, ifilterfalse(player_wins, product(combinations(WEAPONS, 1), list(chain.from_iterable(combinations(ARMOUR, n) for n in xrange(2))), list(chain.from_iterable(combinations(RINGS, n) for n in xrange(3)))))))

from collections import namedtuple
from itertools import ifilter, product
import re

INPUT = """Sprinkles: capacity 2, durability 0, flavor -2, texture 0, calories 3
Butterscotch: capacity 0, durability 5, flavor -3, texture 0, calories 3
Chocolate: capacity 0, durability 0, flavor 5, texture -1, calories 8
Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8"""

Effects = namedtuple('Effects', ['capacity', 'durability', 'flavour', 'texture', 'calories'])

INGREDIENTS = []

for line in INPUT.splitlines():
    INGREDIENTS.append(Effects(*map(int, re.match(r'\w+: capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line).groups())))

combinations = ifilter(lambda seq: sum(seq) == 100, product(xrange(101), xrange(101), xrange(101), xrange(101)))

def calories(ingredient_amounts):
    return sum(map(lambda (ingredient, amount): ingredient.calories * amount, zip(INGREDIENTS, ingredient_amounts)))

combinations = ifilter(lambda amounts: calories(amounts) == 500, combinations) # Comment me out for part 1

def score(ingredient_amounts):
    capacity = sum(map(lambda (ingredient, amount): ingredient.capacity * amount, zip(INGREDIENTS, ingredient_amounts)))
    durability = sum(map(lambda (ingredient, amount): ingredient.durability * amount, zip(INGREDIENTS, ingredient_amounts)))
    flavour = sum(map(lambda (ingredient, amount): ingredient.flavour * amount, zip(INGREDIENTS, ingredient_amounts)))
    texture = sum(map(lambda (ingredient, amount): ingredient.texture * amount, zip(INGREDIENTS, ingredient_amounts)))
    return max(0, capacity) * max(0, durability) * max(0, flavour) * max(0, texture)

print max(map(score, combinations))

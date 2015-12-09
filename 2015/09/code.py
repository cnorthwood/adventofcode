from itertools import permutations
import re

INPUT = """AlphaCentauri to Snowdin = 66
AlphaCentauri to Tambi = 28
AlphaCentauri to Faerun = 60
AlphaCentauri to Norrath = 34
AlphaCentauri to Straylight = 34
AlphaCentauri to Tristram = 3
AlphaCentauri to Arbre = 108
Snowdin to Tambi = 22
Snowdin to Faerun = 12
Snowdin to Norrath = 91
Snowdin to Straylight = 121
Snowdin to Tristram = 111
Snowdin to Arbre = 71
Tambi to Faerun = 39
Tambi to Norrath = 113
Tambi to Straylight = 130
Tambi to Tristram = 35
Tambi to Arbre = 40
Faerun to Norrath = 63
Faerun to Straylight = 21
Faerun to Tristram = 57
Faerun to Arbre = 83
Norrath to Straylight = 9
Norrath to Tristram = 50
Norrath to Arbre = 60
Straylight to Tristram = 27
Straylight to Arbre = 81
Tristram to Arbre = 90"""

LOCATIONS = set()
DISTANCES = {}

for line in INPUT.splitlines():
    match = re.match(r'(\w+) to (\w+) = (\d+)', line)
    start = match.group(1)
    end = match.group(2)
    distance = int(match.group(3))
    DISTANCES[(start, end)] = distance
    DISTANCES[(end, start)] = distance
    LOCATIONS.add(start)
    LOCATIONS.add(end)


def distance(route):
    return sum(DISTANCES[(route[i], route[i + 1])] for i in range(len(route) - 1))

print min(distance(permutation) for permutation in permutations(LOCATIONS))
print max(distance(permutation) for permutation in permutations(LOCATIONS))

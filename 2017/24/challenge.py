#!/usr/bin/env pypy3


def parse(input):
    for part in input.splitlines():
        yield tuple(map(int, part.split('/')))


def build_chains(chain, parts):
    for i, part in enumerate(parts):
        if part[0] == chain[-1]:
            yield from build_chains(chain + list(part), [x for j, x in enumerate(parts) if j != i])
        elif part[1] == chain[-1]:
            yield from build_chains(chain + list(reversed(part)), [x for j, x in enumerate(parts) if j != i])
    yield chain


TEST = list(parse("""0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""))


with open('input.txt') as input_file:
    INPUT = list(parse(input_file.read()))

CHAINS = list(build_chains([0], INPUT))
print("Part One:", max(map(sum, CHAINS)))
print("Part Two:", max((len(chain), sum(chain)) for chain in CHAINS)[1])

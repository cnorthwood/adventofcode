from collections import namedtuple
import re

DF_RE = re.compile(r'/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+\d+T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+\d+%')

GRID = set()
Node = namedtuple('Node', 'x y used avail')

with open('input.txt') as input_file:
    for line in input_file:
        match = DF_RE.match(line)
        if match:
            groups = match.groupdict()
            GRID.add(Node(int(groups['x']), int(groups['y']), int(groups['used']), int(groups['avail'])))


def viable_matches(node):
    if node.used == 0:
        return 0
    else:
        return len(filter(lambda other_node: other_node != node and node.used <= other_node.avail, GRID))

print "Part One:", sum(viable_matches(node) for node in GRID)

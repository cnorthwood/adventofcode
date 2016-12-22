from collections import namedtuple
import re

DF_RE = re.compile(r'/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+\d+%')

GRID = dict()
Node = namedtuple('Node', 'size used avail')

with open('input.txt') as input_file:
    for line in input_file:
        match = DF_RE.match(line)
        if match:
            groups = match.groupdict()
            GRID[int(groups['x']), int(groups['y'])] = Node(int(groups['size']), int(groups['used']), int(groups['avail']))


def viable_matches(node):
    if node.used == 0:
        return 0
    else:
        return len(filter(lambda other_node: other_node != node and node.used <= other_node.avail, GRID.values()))

print "Part One:", sum(viable_matches(node) for node in GRID.values())

EMPTY_NODE = filter(lambda (_, node): node.used == 0, GRID.items())[0]
TOO_FULL = set(filter(lambda (_, node): node.used > EMPTY_NODE[1].size, GRID.items()))
TARGET_LOC = (max(x for x, y in GRID.keys()), 0)

print "Part Two:"
current_y = 0
for y in range(max(_y for _, _y in GRID.keys()) + 1):
    while y > current_y:
        current_y += 1
        print
    for x in range(max(_x for _x, _y in GRID.keys()) + 1):
        if (x,y) in (n[0] for n in TOO_FULL):
            print '#',
        elif GRID[x,y].used == 0:
            print '_',
        elif (x,y) == (0,0):
            print '!',
        elif (x,y) == TARGET_LOC:
            print 'G',
        else:
            print '.',

print
print "Now do by hand"

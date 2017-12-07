#!/usr/bin/env python3

from collections import defaultdict, namedtuple
import re

TEST = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
""".strip().splitlines()

Node = namedtuple('Node', ['id', 'weight', 'children'])
NODE_RE = re.compile(r'(?P<id>\w+) \((?P<weight>\d+)\)( -> (?P<children>.+))?')


def parse_nodes(input):
    for line in input:
        results = NODE_RE.match(line)
        node_id = results.group('id')
        weight = int(results.group('weight'))
        children = results.group('children')
        if children is not None:
            children = children.split(', ')
        else:
            children = []
        yield Node(node_id, weight, children)


def find_root(nodes):
    incoming_links = defaultdict(int)
    for node in nodes:
        incoming_links[node.id] += 0
        for child in node.children:
            incoming_links[child] += 1

    for node, incoming in incoming_links.items():
        if incoming == 0:
            return node


assert find_root(parse_nodes(TEST)) == 'tknk'

with open('input.txt') as input_file:
    print("Part One:", find_root(parse_nodes(input_file.readlines())))

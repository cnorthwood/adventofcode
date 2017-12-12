#!/usr/bin/env python3

from collections import namedtuple
import re

Node = namedtuple('Node', ['id', 'links'])
INPUT_RE = re.compile(r'(?P<id>\d+) <-> (?P<links>.+)')

TEST = """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
""".strip()


def find_connected(node, nodes, seen):
    if node.id not in seen:
        seen.add(node.id)
        for link in node.links:
            find_connected(nodes[link], nodes, seen)
    return seen


def parse(input):
    nodes = {}
    for line in input:
        match = INPUT_RE.match(line)
        nodes[match.group('id')] = Node(match.group('id'), match.group('links').split(', '))
    return nodes


def num_groups(nodes):
    groups_by_node = {
        node_id: ','.join(sorted(find_connected(nodes[node_id], nodes, set())))
        for node_id in nodes.keys()
    }
    return len(set(groups_by_node.values()))


test_nodes = parse(TEST.splitlines())
assert test_nodes['0'] == Node('0', ['2'])
assert len(find_connected(test_nodes['0'], test_nodes, set())) == 6

with open('input.txt') as input_file:
    input_nodes = parse(input_file)

print("Part One:", len(find_connected(input_nodes['0'], input_nodes, set())))

assert num_groups(test_nodes) == 2

print("Part Two:", num_groups(input_nodes))

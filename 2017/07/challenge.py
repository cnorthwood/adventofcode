#!/usr/bin/env python3

from collections import Counter, defaultdict, namedtuple
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


TEST_NODES = list(parse_nodes(TEST))
TEST_NODES_BY_ID = { node.id: node for node in TEST_NODES }
assert find_root(TEST_NODES) == 'tknk'

with open('input.txt') as input_file:
    NODES = list(parse_nodes(input_file.readlines()))
print("Part One:", find_root(NODES))

NODES_BY_ID = {node.id: node for node in NODES}


def node_weight(node_id, nodes_by_id):
    return nodes_by_id[node_id].weight + sum(node_weight(child, nodes_by_id) for child in nodes_by_id[node_id].children)


assert node_weight('ugml', TEST_NODES_BY_ID) == 251
assert node_weight('padx', TEST_NODES_BY_ID) == 243
assert node_weight('fwft', TEST_NODES_BY_ID) == 243


def find_different(items):
    counter = Counter()
    counter.update(items)
    if len(counter) != 2:
        return None, None
    else:
        return items.index(counter.most_common()[-1][0]), counter.most_common()[0][0]


assert find_different([0, 0, 2, 0]) == (2, 0)


def find_unbalanced(root, nodes_by_id, sibling_weight):
    child_weights = [node_weight(child, nodes_by_id) for child in nodes_by_id[root].children]
    different_child_i, expected = find_different(child_weights)
    if different_child_i is None:
        return nodes_by_id[root].weight - node_weight(root, nodes_by_id) + sibling_weight
    else:
        return find_unbalanced(nodes_by_id[root].children[different_child_i], nodes_by_id, expected)

assert find_unbalanced(find_root(TEST_NODES), TEST_NODES_BY_ID, 0) == 60
print("Part Two:", find_unbalanced(find_root(NODES), NODES_BY_ID, 0))

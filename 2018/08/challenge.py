#!/usr/bin/env pypy3

from collections import deque


def parse_nodes(filename):
    with open(filename) as input_file:
        return deque(map(int, input_file.read().strip().split()))


def build_tree(l):
    num_children = l.popleft()
    num_metadata = l.popleft()
    children = [build_tree(l) for _ in range(num_children)]
    metadata = [l.popleft() for _ in range(num_metadata)]
    return children, metadata


def sum_metadata(t):
    if not t:
        return 0
    children, metadata = t
    return sum(sum_metadata(child) for child in children) + sum(metadata)


TEST = build_tree(parse_nodes('test.txt'))
INPUT = build_tree(parse_nodes('input.txt'))


assert(sum_metadata(TEST) == 138)
print("Part One: {}".format(sum_metadata(INPUT)))


def node_value(t):
    children, metadata = t
    if len(children) == 0:
        return sum(metadata)
    else:
        return sum(node_value(children[i - 1]) for i in metadata if 0 < i <= len(children))


assert(node_value(TEST) == 66)
print("Part Two: {}".format(node_value(INPUT)))

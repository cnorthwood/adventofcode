#!/usr/bin/env pypy3

from collections import defaultdict, Counter


def load_graph(filename):
    edges = defaultdict(set)
    with open(filename) as input_file:
        for line in input_file:
            a, b = line.strip().split("-")
            edges[a].add(b)
            edges[b].add(a)
    return edges


def num_routes(graph, can_visit_small_cave):
    routes_to_explore = [(Counter(), ("start",))]
    completed_routes = 0
    while len(routes_to_explore) > 0:
        visit_counter, next_to_explore = routes_to_explore.pop()
        for edge in graph[next_to_explore[-1]]:
            if edge == "start":
                continue
            elif edge == "end":
                completed_routes += 1
            elif edge.isupper() or can_visit_small_cave(edge, visit_counter):
                if not edge.isupper():
                    next_visit_counter = visit_counter.copy()
                    next_visit_counter[edge] += 1
                else:
                    next_visit_counter = visit_counter
                routes_to_explore.append((next_visit_counter, (*next_to_explore, edge)))
    return completed_routes


def can_visit_part_one(edge, visit_counter):
    return visit_counter[edge] == 0


def can_visit_part_two(edge, visit_counter):
    return visit_counter[edge] == 0 or 2 not in visit_counter.values()


GRAPH = load_graph("input.txt")
print(f"Part One: {num_routes(GRAPH, can_visit_part_one)}")
print(f"Part Two: {num_routes(GRAPH, can_visit_part_two)}")

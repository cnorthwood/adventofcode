#!/usr/bin/env python3

from itertools import chain
from math import prod


def parse_rule(line):
    field, values = line.strip().split(": ")
    return field, [(int(value.split("-")[0]), int(value.split("-")[1])) for value in values.split(" or ")]


def parse_ticket(line):
    return [int(value) for value in line.strip().split(",")]


def parse_input(file):
    last_header = "rules:"
    rules = {}
    tickets = []
    my_ticket = []
    for line in file.readlines():
        if line.strip() == "":
            last_header = None
            continue
        if last_header is None:
            last_header = line.strip()
        elif last_header == "rules:":
            field, ranges = parse_rule(line)
            rules[field] = ranges
        elif last_header == "your ticket:":
            my_ticket = parse_ticket(line)
        elif last_header == "nearby tickets:":
            tickets.append(parse_ticket(line))
        else:
            raise ValueError(f"Unknown header {last_header}")
    return rules, my_ticket, tickets


def field_passes_rule(value, ranges):
    return any(low <= value <= high for low, high in ranges)


def invalid_fields(ticket, rules):
    for field in ticket:
        if not any(field_passes_rule(field, ranges) for ranges in rules.values()):
            yield field


def ticket_is_valid(ticket, rules):
    return all(any(field_passes_rule(field, ranges) for ranges in rules.values()) for field in ticket)


def sieve_fields(tickets, rules):
    possible_positions = {field: set(range(len(tickets[0]))) for field in rules.keys()}
    for ticket in tickets:
        for i, value in enumerate(ticket):
            for field, ranges in rules.items():
                if not field_passes_rule(value, ranges):
                    possible_positions[field].remove(i)
    while not all(len(possibilities) == 1 for possibilities in possible_positions.values()):
        for field, possibilities in possible_positions.copy().items():
            if len(possibilities) == 1:
                index = next(iter(possibilities))
                for other_field in possible_positions.keys():
                    if field == other_field:
                        continue
                    possible_positions[other_field] -= {index}
    return {field: next(iter(possibilities)) for field, possibilities in possible_positions.items()}


def my_ticket_value(ticket, positions, prefix="departure"):
    values = []
    for field, position in positions.items():
        if not field.startswith(prefix):
            continue
        values.append(ticket[position])
    return prod(values)


with open("input.txt") as input_file:
    RULES, MY_TICKET, TICKETS = parse_input(input_file)


print(f"Part One: {sum(chain.from_iterable(invalid_fields(ticket, RULES) for ticket in TICKETS))}")
VALID_TICKETS = [ticket for ticket in TICKETS if ticket_is_valid(ticket, RULES)]
print(f"Part Two: {my_ticket_value(MY_TICKET, sieve_fields(VALID_TICKETS, RULES))}")

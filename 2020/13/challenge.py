#!/usr/bin/env python3

from math import prod


with open("input.txt") as input_file:
    lines = input_file.readlines()
    DEPARTURE_TIME = int(lines[0])
    BUSES = [int(bus) if bus != "x" else None for bus in lines[1].split(",")]


def wait_time(timestamp, bus):
    if timestamp % bus == 0:
        return 0
    return bus - (timestamp % bus)


def find_next_bus(timestamp, buses):
    next_bus_id = min((bus for bus in buses if bus is not None), key=lambda bus: wait_time(timestamp, bus))
    return next_bus_id * wait_time(timestamp, next_bus_id)


def crt(buses):
    ns = [bus_id for bus_id in buses if bus_id is not None]
    bs = [bus - i for i, bus in enumerate(buses) if bus is not None]
    N = prod(ns)
    ys = [N // n for n in ns]
    zs = [pow(y, -1, n) for n, y in zip(ns, ys)]
    return sum(prod(byz) for byz in zip(bs, ys, zs)) % N


print(f"Part One: {find_next_bus(DEPARTURE_TIME, BUSES)}")
print(f"Part Two: {crt(BUSES)}")

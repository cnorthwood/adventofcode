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


def test_sequential_timestamp(timestamp, buses, skip):
    for i, bus_id in enumerate(buses):
        if bus_id is None:
            continue
        if (timestamp + i) % bus_id != 0:
            return False, skip
        else:
            skip = prod(bus for bus in buses[:i+1] if bus is not None)
    return True, skip


timestamp = 0
skip = BUSES[0]
while True:
    valid, skip = test_sequential_timestamp(timestamp, BUSES, skip)
    timestamp += skip
    if valid:
        print(timestamp)
        break

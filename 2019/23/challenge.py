#!/usr/bin/env pypy3

from collections import deque
from queue import Empty, Queue
from intcode import IntcodeVM
from threading import Thread


def start_nic(program, address, channels):
    def non_blocking_input():
        if not non_blocking_input.address_sent:
            non_blocking_input.address_sent = True
            return address
        if non_blocking_input.this_packet:
            return non_blocking_input.this_packet.popleft()
        try:
            non_blocking_input.this_packet = channels[address].get(timeout=0.1)
        except Empty:
            return -1
        else:
            return non_blocking_input.this_packet.popleft()
    non_blocking_input.address_sent = False
    non_blocking_input.this_packet = None

    def route_output(val):
        route_output.this_packet.append(val)
        if len(route_output.this_packet) == 3:
            dest, x, y = route_output.this_packet
            route_output.this_packet = []
            channels[dest].put(deque([x, y]))
    route_output.this_packet = []

    IntcodeVM(program, non_blocking_input, route_output).run()


def start(program, nat=False):
    channels = {address: Queue() for address in range(50)}
    channels[255] = Queue()
    for address in range(50):
        Thread(name=f"NIC-{address}", target=start_nic, args=(program, address, channels), daemon=True).start()
    last_sent_packet = None
    last_packet = channels[255].get()
    while nat:
        while not all(queue.empty() for address, queue in channels.items() if address != 255):
            pass
        try:
            while True:
                last_packet = channels[255].get_nowait()
        except Empty:
            pass
        if last_packet == last_sent_packet:
            break
        channels[0].put(last_packet)
        last_sent_packet = deque(last_packet)
        last_packet = channels[255].get()
    return last_packet


with open("input.txt") as input_file:
    PROGRAM = [int(instruction) for instruction in input_file.read().split(",")]

print(f"Part One: {start(PROGRAM)[1]}")
print(f"Part Two: {start(PROGRAM, nat=True)[1]}")

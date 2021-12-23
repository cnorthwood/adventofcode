#!/usr/bin/env python3

from math import prod


def build_bitstream(hex):
    for c in hex:
        val = int(c, 16)
        yield (val & 8) >> 3
        yield (val & 4) >> 2
        yield (val & 2) >> 1
        yield val & 1


def read_bits(bitstream, num_to_take):
    n = 0
    for _ in range(num_to_take):
        n <<= 1
        n |= next(bitstream)
    return n


def take_sub_bitstream(bitstream, length):
    for _ in range(length):
        yield next(bitstream)


def literal_packet(bitstream):
    value = 0
    last_packet = False
    while not last_packet:
        last_packet = not read_bits(bitstream, 1)
        value <<= 4
        value |= read_bits(bitstream, 4)
    return value


def parse_subpackets(bitstream, operator):
    version_total = 0
    values = []
    length_type_id = read_bits(bitstream, 1)
    if length_type_id == 0:
        total_length = read_bits(bitstream, 15)
        sub_bitstream = take_sub_bitstream(bitstream, total_length)
        try:
            while True:
                sub_version, value = parse_packet(sub_bitstream)
                version_total += sub_version
                values.append(value)
        except StopIteration:
            pass
    else:
        num_subpackets = read_bits(bitstream, 11)
        for _ in range(num_subpackets):
            sub_version, value = parse_packet(bitstream)
            version_total += sub_version
            values.append(value)
    return version_total, operator(values)


PACKET_HANDLERS = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda vs: 1 if vs[0] > vs[1] else 0,
    6: lambda vs: 1 if vs[0] < vs[1] else 0,
    7: lambda vs: 1 if vs[0] == vs[1] else 0,
}


def parse_packet(bitstream):
    version = read_bits(bitstream, 3)
    packet_type = read_bits(bitstream, 3)
    if packet_type == 4:
        return version, literal_packet(bitstream)
    else:
        version_sum, value = parse_subpackets(bitstream, PACKET_HANDLERS[packet_type])
        return version + version_sum, value


def parse(raw):
    bitstream = build_bitstream(raw)
    return parse_packet(bitstream)


with open("input.txt") as input_file:
    INPUT = input_file.read().strip()


part_one, part_two = parse(INPUT)
print(f"Part One: {part_one}")
print(f"Part Two: {part_two}")

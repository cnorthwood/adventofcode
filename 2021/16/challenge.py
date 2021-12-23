#!/usr/bin/env python3

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
    n = 0
    last_packet = False
    while not last_packet:
        last_packet = not read_bits(bitstream, 1)
        n <<= 4
        n |= read_bits(bitstream, 4)
    return 0


def unknown_operator(bitstream):
    version_total = 0
    length_type_id = read_bits(bitstream, 1)
    if length_type_id == 0:
        total_length = read_bits(bitstream, 15)
        sub_bitstream = take_sub_bitstream(bitstream, total_length)
        try:
            while True:
                version_total += parse_packet(sub_bitstream)
        except StopIteration:
            pass
    else:
        num_subpackets = read_bits(bitstream, 11)
        for _ in range(num_subpackets):
            version_total += parse_packet(bitstream)
    return version_total


PACKET_HANDLERS = {
    4: literal_packet,
}


def parse_packet(bitstream):
    version = read_bits(bitstream, 3)
    packet_type = read_bits(bitstream, 3)
    return version + PACKET_HANDLERS.get(packet_type, unknown_operator)(bitstream)


def parse(raw):
    bitstream = build_bitstream(raw)
    return parse_packet(bitstream)


with open("input.txt") as input_file:
    INPUT = input_file.read().strip()

print(f"Part One: {parse(INPUT)}")

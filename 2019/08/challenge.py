#!/usr/bin/env python3
# coding=utf8

import sys

WIDTH = 25
HEIGHT = 6
CHARS = {
    "0": " ",
    "1": "█",
}


def num_digits(layer, digit):
    return len([d for d in layer if d == digit])


def decode_image(layers):
    decoded = {}
    for layer in layers:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                pixel = layer[y * WIDTH + x]
                if (x, y) not in decoded and pixel != "2":
                    decoded[x, y] = pixel
    return decoded


def print_image(image):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            sys.stdout.write(CHARS[image[x, y]])
        sys.stdout.write("\n")
    sys.stdout.write("\n")


with open("input.txt") as input_file:
    INPUT = input_file.read().strip()

layers = [INPUT[i:i + (WIDTH*HEIGHT)] for i in range(0, len(INPUT), WIDTH * HEIGHT)]
fewest_zero_layer = min(layers, key=lambda layer: num_digits(layer, "0"))

print(f"Part One: {num_digits(fewest_zero_layer, '1') * num_digits(fewest_zero_layer, '2')}")
print("Part Two:")
print_image(decode_image(layers))

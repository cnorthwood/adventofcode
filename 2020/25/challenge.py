#!/usr/bin/env pypy3

from itertools import count


def find_loop_size(pub_key1, pub_key2):
    potential_key = 1
    for i in count(1):
        potential_key = (potential_key * 7) % 20201227
        if potential_key == pub_key1:
            return pub_key2, i
        if potential_key == pub_key2:
            return pub_key1, i


with open("input.txt") as input_file:
    pub_key1 = int(next(input_file).strip())
    pub_key2 = int(next(input_file).strip())
KEY, LOOP_SIZE = find_loop_size(pub_key1, pub_key2)
enc_key = 1
for _ in range(LOOP_SIZE):
    enc_key = (enc_key * KEY) % 20201227
print(enc_key)

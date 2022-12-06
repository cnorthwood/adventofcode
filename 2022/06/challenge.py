#!/usr/bin/env python3

def find_start_of_message_marker(message, marker_size):
    for i in range(len(message)):
        if len(set(message[i:i+marker_size])) == marker_size:
            return i + marker_size


with open("input.txt") as input_file:
    INPUT = input_file.read().strip()


print(f"Part One: {find_start_of_message_marker(INPUT, 4)}")
print(f"Part One: {find_start_of_message_marker(INPUT, 14)}")

#!/usr/bin/env pypy3

from collections import deque


with open('input.txt') as input_file:
    input_tokens = input_file.read().strip().split()
    NUM_PLAYERS = int(input_tokens[0])
    LAST_MARBLE = int(input_tokens[6])


def simulate(num_players, last_marble):
    marbles = deque()
    scores = {player: 0 for player in range(num_players)}
    for marble in range(last_marble + 1):
        if marble == 0:
            marbles.append(0)
        elif marble % 23 == 0:
            marbles.rotate(7)
            scores[marble % num_players] += marble + marbles.popleft()
        else:
            marbles.rotate(-2)
            marbles.appendleft(marble)
    return max(scores.values())


assert(simulate(9, 25) == 32)
assert(simulate(10, 1618) == 8317)
assert(simulate(13, 7999) == 146373)
assert(simulate(17, 1104) == 2764)
assert(simulate(21, 6111) == 54718)
assert(simulate(30, 5807) == 37305)
print("Part One: {}".format(simulate(NUM_PLAYERS, LAST_MARBLE)))
print("Part Two: {}".format(simulate(NUM_PLAYERS, LAST_MARBLE * 100)))

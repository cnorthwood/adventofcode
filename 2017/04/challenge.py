#!/usr/bin/env python3


def valid(words):
    words = words.split()
    return len(set(words)) == len(words)


assert valid("aa bb cc dd ee")
assert not valid("aa bb cc dd aa")
assert valid("aa bb cc dd aaa")

with open('input.txt') as input:
    print("Part One:", len(list(filter(valid, input.readlines()))))


def valid_anagram(words):
    words = [''.join(sorted(word)) for word in words.split()]
    return len(set(words)) == len(words)


assert valid_anagram("abcde fghij")
assert not valid_anagram("abcde xyz ecdab")
assert valid_anagram("a ab abc abd abf abj")
assert valid_anagram("iiii oiii ooii oooi oooo")
assert not valid_anagram("oiii ioii iioi iiio")


with open('input.txt') as input:
    print("Part Two:", len(list(filter(valid_anagram, input.readlines()))))

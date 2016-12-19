from collections import deque

INPUT = 3004953


def left_elves(sorted_elves):
    return {sorted_elves[(i + 1) % len(sorted_elves)] for i in xrange(0, len(sorted_elves), 2)}


def opposite_elves(sorted_elves):
    deleted_elves = set()
    for i, elf in enumerate(sorted_elves):
        if elf not in deleted_elves:
            steal_i = ((i + len(sorted_elves)) / 2) % len(sorted_elves)
            # print "{} steals from {}".format(elf, sorted_elves[steal_i])
            deleted_elves.add(sorted_elves[steal_i])
            sorted_elves = sorted_elves[:steal_i] + sorted_elves[steal_i + 1:]
    return deleted_elves


def last_elf_remaining(strategy, num_elves=INPUT):
    elves = {i + 1 for i in xrange(num_elves)}

    while len(elves) > 1:
        print "{} left this round".format(len(elves))
        elves -= strategy(sorted(elves))
    return elves.pop()

assert last_elf_remaining(left_elves, 5) == 3
assert last_elf_remaining(opposite_elves, 5) == 2

print "Part One:", last_elf_remaining(left_elves)
print "Part Two:", last_elf_remaining(opposite_elves)

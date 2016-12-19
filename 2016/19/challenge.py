INPUT = 3004953

ELVES = {i: 1 for i in xrange(INPUT)}

while len(ELVES) > 1:
    print "{} left this round".format(len(ELVES))
    for i in sorted(ELVES.keys()):
        if i in ELVES:
            for j in xrange(1, INPUT):
                steal_from = (i + j) % INPUT
                if steal_from in ELVES:
                    # print "{} stole from {}".format(i, steal_from)
                    ELVES[i] += ELVES[steal_from]
                    del ELVES[steal_from]
                    break


print "Part One:", ELVES.keys()[0] + 1

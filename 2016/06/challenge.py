from collections import Counter

with open('input.txt') as input:
    MESSAGES = input.readlines()

counters = []
for i in range(max(map(len, MESSAGES))):
    counters.append(Counter())

for line in MESSAGES:
    for i, c in enumerate(line):
        counters[i][c] += 1

print 'Part 1:', ''.join(counter.most_common()[0][0] for counter in counters)
print 'Part 2:', ''.join(counter.most_common()[-1][0] for counter in counters)

numbers = set()


with open('input.txt') as input_file:
    for line in input_file:
        parts = line.split('-')
        numbers.add((int(parts[0]), int(parts[1])))

numbers = sorted(numbers)

merged_overlaps = []

current_interval = (0, 1)
for start, end in numbers:
    if current_interval[0] <= start <= current_interval[1] + 1:
        if end > current_interval[1]:
            current_interval = (current_interval[0], end)
    else:
        merged_overlaps.append(current_interval)
        current_interval = (start, end)
merged_overlaps.append(current_interval)


print "Part One:", merged_overlaps[0][1] + 1

num_allowed = 0

for start, end in zip([0] + [end + 1 for start, end in merged_overlaps], [start for start, end in merged_overlaps] + [2**32]):
    num_allowed += end - start

print "Part Two:", num_allowed

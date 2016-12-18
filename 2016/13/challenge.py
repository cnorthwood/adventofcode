def is_open((x, y), seed=1362):
    if x < 0 or y < 0:
        return False
    else:
        return len(filter(lambda c: c == '1', '{0:b}'.format(x*x + 3*x + 2*x*y + y + y*y + seed))) % 2 == 0

assert is_open((0, 0), seed=10)
assert is_open((1, 1), seed=10)
assert not is_open((1, 0), seed=10)


def generate_options((x, y)):
    yield x, y-1
    yield x-1, y
    yield x+1, y
    yield x, y+1


i = 0
options = {(1, 1)}
seen_options = set(options)
while (31, 39) not in options:
    print "Iteration {}: {} to check".format(i, len(options))
    next_options = set()
    for option in options:
        next_options |= frozenset(filter(is_open, generate_options(option)))
    next_options -= seen_options
    seen_options |= next_options
    options = next_options
    if len(options) == 0:
        print "Out of options"
        break
    i += 1

print "Part One:", i

locations = {(1, 1)}
for i in range(50):
    for location in frozenset(locations):
        locations |= frozenset(filter(is_open, generate_options(location)))
print "Part Two", len(locations)

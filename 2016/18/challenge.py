import itertools

INPUT = '.^^.^^^..^.^..^.^^.^^^^.^^.^^...^..^...^^^..^^...^..^^^^^^..^.^^^..^.^^^^.^^^.^...^^^.^^.^^^.^.^^.^.'


def is_safe(left, centre, right):
    if not left and not centre and right:
        return False
    elif not centre and not right and left:
        return False
    elif not left and right and centre:
        return False
    elif not right and left and centre:
        return False
    else:
        return True


def generate_row(previous_row):
    return [is_safe(previous_row[i-1], previous_row[i], previous_row[i+1]) for i in range(1, len(previous_row) - 1)]


def generate_floor(rows):
    floor = []
    floor.append([True] + [True if c == '.' else False for c in INPUT] + [True])
    while len(floor) < rows:
        floor.append([True] + generate_row(floor[-1]) + [True])

    return [row[1:-1] for row in floor]

print "Part One:", len(filter(lambda t: t, itertools.chain(*generate_floor(40))))
print "Part Two:", len(filter(lambda t: t, itertools.chain(*generate_floor(400000))))

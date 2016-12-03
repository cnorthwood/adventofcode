from itertools import izip_longest

with open('input.txt') as input:
    TRIANGLE_ROWS = [map(int, line.split()) for line in input]


# From https://docs.python.org/2.7/library/itertools.html#recipes
def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def convert_into_columns(triangles):
    for r1, r2, r3 in grouper(3, triangles):
        for i in range(0, 3):
            yield (r1[i], r2[i], r3[i])


def valid_triangles(triangles):
    sorted_triangles = (sorted(triangle) for triangle in triangles)
    return filter(lambda (a, b, c): a + b > c, sorted_triangles)

print "Part 1:", len(valid_triangles(TRIANGLE_ROWS))
print "Part 2:", len(valid_triangles(convert_into_columns(TRIANGLE_ROWS)))

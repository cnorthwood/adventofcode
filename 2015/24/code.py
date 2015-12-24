from operator import mul

INPUT = """1
2
3
5
7
13
17
19
23
29
31
37
41
43
53
59
61
67
71
73
79
83
89
97
101
103
107
109
113"""

PACKAGES = set(map(int, INPUT.splitlines()))


def pack_bucket_a():
    bucket = set()
    target_bucket_size = sum(PACKAGES) / 3

    for package in sorted(PACKAGES, reverse=True):
        if sum(bucket) + package > target_bucket_size:
            continue

        bucket.add(package)
        if sum(bucket) == target_bucket_size:
            return bucket



def pack_bucket_b(bucket, packages):
    target_bucket_size = sum(PACKAGES) / 4

    for i, package in enumerate(packages):
        if sum(bucket) + package > target_bucket_size:
            continue

        potential_bucket = set(bucket)
        bucket.add(package)

        if sum(bucket) == target_bucket_size:
            return [bucket] + pack_bucket_b(potential_bucket, packages[i+1:])
        else:
            return pack_bucket_b(bucket, packages[i+1:]) + pack_bucket_b(potential_bucket, packages[i+1:])

    return []


print "Part One:", reduce(mul, pack_bucket_a())
print "Part Two:", min(map(lambda b: reduce(mul, b), pack_bucket_b(set(), sorted(PACKAGES, reverse=True))))

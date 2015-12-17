INPUT = """50
44
11
49
42
46
18
32
26
40
21
7
18
43
10
47
36
24
22
40"""

BUCKETS = map(int, INPUT.splitlines())

from itertools import chain, combinations

bucket_combinations = chain.from_iterable(combinations(BUCKETS, n+1) for n in xrange(len(BUCKETS)))
good_buckets = filter(lambda buckets: sum(buckets) == 150, bucket_combinations)

print "Part One:", len(good_buckets)

smallest_bucket = min(map(len, good_buckets))
small_bucket_combinations = filter(lambda buckets: len(buckets) == smallest_bucket, good_buckets)

print "Part Two", len(small_bucket_combinations)

from hashlib import md5
from itertools import count
import re

SALT = 'ihaygndm'
TRIP_MATCH = re.compile(r'(?P<c>.)(?P=c)(?P=c)')

def memoize(f):
    results = {}
    def memoized(i):
        if i not in results:
            results[i] = f(i)
        return results[i]
    return memoized

@memoize
def genhash(i):
    hashed = md5(SALT + str(i)).hexdigest()
    for _ in range(2016):
        hashed = md5(hashed).hexdigest()
    return hashed


def in_next_1000(char, i):
    for j in range(1, 1001):
        if char * 5 in genhash(i+j):
            return True
    else:
        return False

found = 0
for i in count():
    hashed = genhash(i)
    match = TRIP_MATCH.search(hashed)
    if match and in_next_1000(match.group('c'), i):
        found += 1
    if found == 64:
        print "Part Two:", i
        break

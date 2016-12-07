from itertools import chain
import re

PAIR_CHECK = re.compile(r'(?P<char1>.)(?P<char2>(?!(?P=char1)).)(?P=char2)(?P=char1)')
TRIP_CHECK = re.compile(r'(?=((?P<char1>.)(?P<char2>(?!(?P=char1)).)(?P=char1)))')


def parse_line(line):
    parts = re.split(r'[\[\]]', line)
    return parts[::2], parts[1::2]


def supports_tls((outer, inner)):
    return True in map(lambda p: bool(PAIR_CHECK.search(p)), outer) and \
           True not in map(lambda p: bool(PAIR_CHECK.search(p)), inner)


def supports_ssl((outer, inner)):
    triples = set(chain(*(map(lambda r: r[0], TRIP_CHECK.findall(part)) for part in outer)))
    if len(triples) == 0:
        return False
    for triple in triples:
        check_triple = triple[1] + triple[0] + triple[1]
        for inner_part in inner:
            if check_triple in inner_part:
                return True


assert supports_tls(parse_line('abba[mnop]qrst'))
assert not supports_tls(parse_line('abcd[bddb]xyyx'))
assert not supports_tls(parse_line('aaaa[qwer]tyui'))
assert supports_tls(parse_line('ioxxoj[asdfgh]zxcvbn'))

assert supports_ssl(parse_line('aba[bab]xyz'))
assert not supports_ssl(parse_line('xyx[xyx]xyx'))
assert supports_ssl(parse_line('aaa[kek]eke'))
assert supports_ssl(parse_line('zazbz[bzb]cdb'))

with open('input.txt') as input:
    lines = map(parse_line, input)
    print "Part 1:", len(filter(supports_tls, lines))
    print "Part 2:", len(filter(supports_ssl, lines))

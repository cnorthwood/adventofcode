import re

EXPANSION_CHECK = re.compile(r'(?P<pre>[^\(]*)(\((?P<consume>\d+)x(?P<repeat>\d+)\))?')


def decompress(text):
    i = 0
    decompressed = []
    while i < len(text):
        expansion = EXPANSION_CHECK.match(text[i:])
        pre = expansion.groupdict()['pre']
        consume = expansion.groupdict()['consume']
        i += len(pre)
        decompressed.append(pre)
        if consume:
            repeat = expansion.groupdict()['repeat']
            i += len(consume) + len(repeat) + 3
            decompressed.extend([text[i:i + int(consume)]] * int(repeat))
            i += int(consume)
    return ''.join(decompressed)


def decompress2(text):
    while '(' in text:
        text = decompress(text)
        print len(text)
    return text

assert decompress('ADVENT') == 'ADVENT'
assert decompress('A(1x5)BC') == 'ABBBBBC'
assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
assert decompress('(6x1)(1x3)A') == '(1x3)A'
assert decompress('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'

assert decompress2('(3x3)XYZ') == 'XYZXYZXYZ'
assert decompress2('X(8x2)(3x3)ABCY') == 'XABCABCABCABCABCABCY'
assert len(decompress2('(27x12)(20x12)(13x14)(7x10)(1x12)A')) == 241920
assert len(decompress2('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')) == 445

with open('input.txt') as input:
    text = input.read().strip()
    print "Part 1:", len(decompress(text))
    # print "Part 2:", len(decompress2(text))

import re

EXPANSION_CHECK = re.compile(r'(?P<pre>[^\(]*)(\((?P<consume>\d+)x(?P<repeat>\d+)\))?')


def decompress_length(text, recurse):
    l = 0
    while text:
        expansion = EXPANSION_CHECK.match(text)
        pre_length = len(expansion.groupdict()['pre'])
        l += pre_length
        text = text[pre_length:]
        if expansion.groupdict()['consume']:
            consume = int(expansion.groupdict()['consume'])
            repeat = int(expansion.groupdict()['repeat'])
            text = text[len('({}x{})'.format(consume, repeat)):]
            if recurse:
                l += decompress_length(text[:consume], recurse) * repeat
            else:
                l += consume * repeat
            text = text[consume:]
    return l

assert decompress_length('ADVENT', False) == 6
assert decompress_length('A(1x5)BC', False) == 7
assert decompress_length('(3x3)XYZ', False) == 9
assert decompress_length('A(2x2)BCD(2x2)EFG', False) == 11
assert decompress_length('(6x1)(1x3)A', False) == 6
assert decompress_length('X(8x2)(3x3)ABCY', False) == 18

assert decompress_length('(3x3)XYZ', True) == 9
assert decompress_length('X(8x2)(3x3)ABCY', True) == 20
assert decompress_length('(27x12)(20x12)(13x14)(7x10)(1x12)A', True) == 241920
assert decompress_length('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', True) == 445


with open('input.txt') as input:
    text = input.read().strip()
    print "Part 1:", decompress_length(text, False)
    print "Part 2:", decompress_length(text, True)

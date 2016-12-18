def dragon(a):
    b = ''.join('0' if c == '1' else '1' for c in reversed(a))
    return a + '0' + b

assert dragon('1') == '100'
assert dragon('0') == '001'
assert dragon('11111') == '11111000000'
assert dragon('111100001010') == '1111000010100101011110000'


def checksum(data):
    check = ''.join('1' if a == b else '0' for a, b in zip(data[::2], data[1::2]))
    if len(check) % 2 == 0:
        return checksum(check)
    else:
        return check

assert checksum('110010110100') == '100'


def generate_checksum_for_random_length(input, l):
    while len(input) < l:
        input = dragon(input)
    return checksum(input[:l])


INPUT = '01111010110010011'
print "Part One:", generate_checksum_for_random_length(INPUT, 272)
print "Part Two:", generate_checksum_for_random_length(INPUT, 35651584)

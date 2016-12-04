from collections import Counter
import re

ROOM_RE = re.compile(r'(?P<room_id>[a-z\-]+)-(?P<sector>\d+)\[(?P<checksum>[a-z]{5})\]')


def load_rooms():
    with open('input.txt') as input:
        for line in input:
            yield ROOM_RE.match(line).groupdict()


def real_room(room):
    room_id = room['room_id'].replace('-', '')
    checksum = room['checksum']
    letters = Counter(room_id)
    sorted_letters = sorted(letters.most_common(), key=lambda (letter, count): (-count, letter))
    return list(checksum) == [letter for letter, count in sorted_letters[:5]]

assert real_room({'room_id': 'aaaaa-bbb-z-y-x', 'checksum': 'abxyz'})
assert real_room({'room_id': 'a-b-c-d-e-f-g-h', 'checksum': 'abcde'})
assert real_room({'room_id': 'not-a-real-room', 'checksum': 'oarel'})
assert not real_room({'room_id': 'totally-real-room', 'checksum': 'decoy'})

real_rooms = filter(real_room, load_rooms())

print "Part 1:", sum(map(lambda room: int(room['sector']), real_rooms))


def decrypt(ciphertext, key):
    deciphered = ''
    for letter in ciphertext:
        if letter == '-':
            deciphered += ' '
        else:
            deciphered += chr((ord(letter) - 97 + int(key)) % 26 + 97)
    return deciphered


assert decrypt('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'

for room in real_rooms:
    if decrypt(room['room_id'], room['sector']) == 'northpole object storage':
        print "Part 2:", room['sector']
        break
else:
    print "Part Two: unable to find north pole objects"

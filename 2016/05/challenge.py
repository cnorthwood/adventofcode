from hashlib import md5
from itertools import count

DOOR_ID = 'uqwqemis'

password = [None] * 8

for i in count():
    hash = md5(DOOR_ID + str(i)).hexdigest()
    if hash[:5] == '00000':
        position = int(hash[5], 16)
        if position < 8 and password[position] is None:
            print password
            password[position] = hash[6]
    if len(filter(lambda l: l is None, password)) == 0:
        break

print "Part 2:", ''.join(password)

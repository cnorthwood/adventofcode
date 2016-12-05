from hashlib import md5
from itertools import count

DOOR_ID = 'uqwqemis'

password = ''

for i in count():
    hash = md5(DOOR_ID + str(i)).hexdigest()
    if hash[:5] == '00000':
        password += hash[5]
    if len(password) == 8:
        break

print "Part 1:", password

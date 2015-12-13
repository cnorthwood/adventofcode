import re
from string import ascii_lowercase

INPUT = "hepxcrrq"

REQUIRED_SUBSTRINGS = set(ascii_lowercase[i:i+3] for i in range(len(ascii_lowercase) - 2))

def to_ascii(n):
    result = ''
    while n > 0:
        result = ascii_lowercase[n % len(ascii_lowercase)] + result
        n /= len(ascii_lowercase)
    return result

def to_int(s):
    result = 0
    for i, c in enumerate(reversed(s)):
        result += ascii_lowercase.index(c) * (len(ascii_lowercase) ** i)
    return result

def check_password(password):
    if 'i' in password or 'o' in password or 'l' in password: return False
    if re.search(r'(.)\1.*(.)\2', password) is None: return False
    for substring in REQUIRED_SUBSTRINGS:
        if substring in password: return True
    return False

assert(check_password("hijklmmn") is False)
assert(check_password("abbceffg") is False)
assert(check_password("abbcegjk") is False)
assert(check_password("abcdffaa") is True)
assert(check_password("ghjaabcc") is True)

current_password = to_int(INPUT)
while check_password(to_ascii(current_password)) is False:
    current_password += 1

print "Part One: ", to_ascii(current_password)

current_password += 1
while check_password(to_ascii(current_password)) is False:
    current_password += 1

print "Part Two: ", to_ascii(current_password)

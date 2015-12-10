INPUT = "1113222113"

def expand(input):
    output = ""
    last_char = input[0]
    last_char_nos = 0
    for c in input:
        if c == last_char:
            last_char_nos += 1
        else:
            output += str(last_char_nos) + last_char
            last_char = c
            last_char_nos = 1
    output += str(last_char_nos) + last_char
    return output

for i in range(50):
    INPUT = expand(INPUT)

print len(INPUT)

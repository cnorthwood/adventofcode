from itertools import count


def calc(target_x, target_y):
    for i in count():
        for x in range(1, i):
            y = i - x
            if (x,y) == (1,1):
                code = 20151125
            else:
                code = (code * 252533) % 33554393
            if x == target_x and y == target_y:
                return code

assert(calc(1,1) == 20151125)
assert(calc(2,1) == 18749137)

print calc(3019, 3010)

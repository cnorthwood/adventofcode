#!/usr/bin/env python3

INPUT = list(map(int, '4	10	4	1	8	4	9	14	5	1	14	15	0	15	3	5'.split()))


def get_biggest_block(blocks):
    return max(enumerate(blocks), key=lambda x: x[1])[0]


assert get_biggest_block([0, 2, 7, 0]) == 2
assert get_biggest_block([2, 4, 1, 2]) == 1
assert get_biggest_block([3, 1, 2, 3]) == 0


def rebalance(blocks):
    i = get_biggest_block(blocks)
    n = blocks[i]
    blocks[i] = 0
    while n:
        i += 1
        blocks[i % len(blocks)] += 1
        n -= 1
    return blocks


assert rebalance([0, 2, 7, 0]) == [2, 4, 1, 2]
assert rebalance([2, 4, 1, 2]) == [3, 1, 2, 3]
assert rebalance([3, 1, 2, 3]) == [0, 2, 3, 4]
assert rebalance([0, 2, 3, 4]) == [1, 3, 4, 1]
assert rebalance([1, 3, 4, 1]) == [2, 4, 1, 2]


def find_loop(blocks):
    balances = 0
    seen = { ','.join(map(str, blocks)) }
    while True:
        blocks = rebalance(blocks)
        balances += 1
        blocks_str = ','.join(map(str, blocks))
        if blocks_str in seen:
            break
        seen.add(blocks_str)
    return balances, blocks


assert find_loop([0, 2, 7, 0]) == (5, [2, 4, 1, 2])
assert find_loop([2, 4, 1, 2]) == (4, [2, 4, 1, 2])


to_first_loop, loop_start = find_loop(INPUT)

print("Part One:", to_first_loop)

to_second_loop, loop_start = find_loop(loop_start)

print("Part Two:", to_second_loop)

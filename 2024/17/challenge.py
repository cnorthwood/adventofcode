#!/usr/bin/env -S python3 -S
from math import inf


def load_input(input_filename):
    a = None
    b = None
    c = None

    with open(input_filename) as input_file:
        for line in input_file:
            if line.startswith("Register A"):
                a = int(line.split(":")[1].strip())
            if line.startswith("Register B"):
                b = int(line.split(":")[1].strip())
            if line.startswith("Register C"):
                c = int(line.split(":")[1].strip())
            if line.startswith("Program"):
                program = list(map(int, line.split(":")[1].strip().split(",")))

    return program, a, b, c


def main(init_a, init_b, init_c):
    state = {
        "ip": 0,
        "a": init_a,
        "b": init_b,
        "c": init_c,
        "output": []
    }

    combo_operands = {
        0: lambda: 0,
        1: lambda: 1,
        2: lambda: 2,
        3: lambda: 3,
        4: lambda: state["a"],
        5: lambda: state["b"],
        6: lambda: state["c"],
    }

    def adv(x):
        state["a"] = state["a"] // (2 ** combo_operands[x]())
        state["ip"] += 2

    def bxl(x):
        state["b"] = state["b"] ^ x
        state["ip"] += 2

    def bst(x):
        state["b"] = combo_operands[x]() % 8
        state["ip"] += 2

    def jnz(x):
        if state["a"] == 0:
            state["ip"] += 2
        else:
            state["ip"] = x

    def bxc(_):
        state["b"] = state["b"] ^ state["c"]
        state["ip"] += 2

    def out(x):
        state["output"].append(combo_operands[x]() % 8)
        state["ip"] += 2

    def bdv(x):
        state["b"] = state["a"] // (2 ** combo_operands[x]())
        state["ip"] += 2

    def cdv(x):
        state["c"] = state["a"] // (2 ** combo_operands[x]())
        state["ip"] += 2

    operators = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv,
    }

    while 0 <= state["ip"] < len(PROGRAM):
        operators[PROGRAM[state["ip"]]](PROGRAM[state["ip"] + 1])

    return state["output"]

# nfc what this does, basically stolen from https://github.com/categoraal/adventofcode2024/blob/main/day17.py
def part2(test_seed=0, program_i=15):
    possibilities = [inf]
    if program_i == -1:
        return test_seed

    for i in range(8):
        test_a = test_seed + i * 8 ** program_i
        output = main(init_a=test_a, init_b=0, init_c=0)
        if len(output) != len(PROGRAM):
            continue
        if output[program_i] == PROGRAM[program_i]:
            possibilities.append(part2(test_a, program_i - 1))
    return min(possibilities)


PROGRAM, INIT_A, INIT_B, INIT_C = load_input("input.txt")
print(f"Part One: {','.join(map(str,main(INIT_A, INIT_B, INIT_C)))}")
print(f"Part Two: {part2()}")

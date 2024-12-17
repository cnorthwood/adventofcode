#!/usr/bin/env -S python3 -S

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


def main(program, init_a, init_b, init_c):
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

    while 0 <= state["ip"] < len(program):
        operators[program[state["ip"]]](program[state["ip"] + 1])

    return ",".join(map(str, state["output"]))

print(f"Part One: {main(*load_input('input.txt'))}")

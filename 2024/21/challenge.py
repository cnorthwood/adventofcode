#!/usr/bin/env -S pypy3 -S

from enum import Enum

class RobotControlButtons(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    ACTIVATE = "A"


class Robot:
    def _move_to(self, button):
        target = self._buttons[button]

        while target[0] > self._state[0]:
            self._state = self._state[0] + 1, self._state[1]
            yield RobotControlButtons.RIGHT

        while target[1] < self._state[1]:
            self._state = self._state[0], self._state[1] - 1
            yield RobotControlButtons.UP

        while target[1] > self._state[1]:
            self._state = self._state[0], self._state[1] + 1
            yield RobotControlButtons.DOWN

        while target[0] < self._state[0]:
            self._state = self._state[0] - 1, self._state[1]
            yield RobotControlButtons.LEFT

        yield RobotControlButtons.ACTIVATE


class KeypadControllingRobot(Robot):
    _buttons = {
        "7": (0, 0),
        "8": (1, 0),
        "9": (2, 0),
        "4": (0, 1),
        "5": (1, 1),
        "6": (2, 1),
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "0": (1, 3),
        "A": (2, 3),
    }

    def __init__(self):
        self._state = self._buttons["A"]

    def enter_code(self, code):
        for c in code:
            yield from self._move_to(c)


class RobotControllingRobot(Robot):
    _buttons = {
        RobotControlButtons.UP: (1, 0),
        RobotControlButtons.ACTIVATE: (2, 0),
        RobotControlButtons.LEFT: (0, 1),
        RobotControlButtons.DOWN: (1, 1),
        RobotControlButtons.RIGHT: (2, 1),
    }

    def __init__(self, robot_under_control):
        self._state = self._buttons[RobotControlButtons.ACTIVATE]
        self._robot_under_control = robot_under_control

    def enter_code(self, code):
        for button_press_needed in self._robot_under_control.enter_code(code):
            yield from self._move_to(button_press_needed)


def part1(code):
    keypad_robot = KeypadControllingRobot()
    intermediate_robot = RobotControllingRobot(robot_under_control=keypad_robot)
    my_robot = RobotControllingRobot(robot_under_control=intermediate_robot)

    num_part = int(code[:-1])
    print("".join(button.value for button in my_robot.enter_code(code)))
    return num_part * sum(1 for _ in my_robot.enter_code(code))

assert(part1("029A") == 68 * 29)
assert(part1("980A") == 60 * 980)
assert(part1("179A") == 68 * 179)
assert(part1("456A") == 64 * 456)
assert(part1("379A") == 64 * 379)

with open("input.txt") as input_file:
    INPUT = [line.strip() for line in input_file]
print(f"Part One: {sum(part1(code) for code in INPUT)}")

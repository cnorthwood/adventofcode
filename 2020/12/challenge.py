#!/usr/bin/env python3

with open("input.txt") as input_file:
    INPUT = [(line[0], int(line[1:])) for line in input_file.readlines()]


def simulator(instructions):
    heading = 90
    x = 0
    y = 0
    for command, value in instructions:
        if command == "N" or command == "F" and heading == 0:
            y += value
        elif command == "S" or command == "F" and heading == 180:
            y -= value
        elif command == "E" or command == "F" and heading == 90:
            x += value
        elif command == "W" or command == "F" and heading == 270:
            x -= value
        elif command == "R":
            heading = (heading + value) % 360
        elif command == "L":
            heading = (heading - value) % 360
        else:
            raise ValueError(f"unrecognised instruction {command}{value} {heading}")
    return abs(x) + abs(y)


def waypoint_simulator(instructions):
    ship_x = 0
    ship_y = 0
    waypoint_x = 10
    waypoint_y = 1
    for command, value in instructions:
        if command == "N":
            waypoint_y += value
        elif command == "S":
            waypoint_y -= value
        elif command == "E":
            waypoint_x += value
        elif command == "W":
            waypoint_x -= value
        elif command == "L":
            dx = waypoint_x
            dy = waypoint_y
            if value == 90:
                waypoint_x = -dy
                waypoint_y = dx
            elif value == 180:
                waypoint_x = -dx
                waypoint_y = -dy
            elif value == 270:
                waypoint_x = dy
                waypoint_y = -dx
        elif command == "R":
            dx = waypoint_x
            dy = waypoint_y
            if value == 270:
                waypoint_x = -dy
                waypoint_y = dx
            elif value == 180:
                waypoint_x = -dx
                waypoint_y = -dy
            elif value == 90:
                waypoint_x = dy
                waypoint_y = -dx
        elif command == "F":
            ship_x += waypoint_x * value
            ship_y += waypoint_y * value
    return abs(ship_x) + abs(ship_y)


print(f"Part One: {simulator(INPUT)}")
print(f"Part Two: {waypoint_simulator(INPUT)}")

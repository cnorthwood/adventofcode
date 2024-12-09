#!/usr/bin/env -S pypy3 -S

def build_disk_layout(layout):
    contents = [0] * layout[0]
    for free_space, (file_id, length) in zip(layout[1::2], enumerate(layout[2::2])):
        contents.extend([None] * free_space)
        contents.extend([file_id + 1] * length)
    return contents


def defrag(contents):
    contents = contents[:]
    try:
        while next_free := contents.index(None):
            item = contents.pop()
            if item is None:
                continue
            contents[next_free] = item
    except ValueError:
        return contents


def checksum(contents):
    return sum(i * file_id for i, file_id in enumerate(contents))


with open("input.txt") as input_file:
    INPUT = list(map(int, input_file.read().strip()))


print(f"Part One: {checksum(defrag(build_disk_layout(INPUT)))}")

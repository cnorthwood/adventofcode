#!/usr/bin/env -S pypy3 -S

from pprint import pprint


def build_disk_layout(layout):
    contents = [0] * layout[0]
    for free_space, (file_id, length) in zip(layout[1::2], enumerate(layout[2::2])):
        contents.extend([None] * free_space)
        contents.extend([file_id + 1] * length)
    return contents


def compact(contents):
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
    return sum(i * file_id for i, file_id in enumerate(contents) if file_id != None)


def build_disk_map(layout):
    # dict of start index to tuple of ID, length
    disk_map = {0: (0, layout[0])}
    i = layout[0]
    for free_space, (file_id, length) in zip(layout[1::2], enumerate(layout[2::2])):
        if free_space > 0:
            disk_map[i] = (None, free_space)
            i += free_space
        disk_map[i] = (file_id + 1, length)
        i += length
    return disk_map


def defrag_file(disk_map, target_file_id):
    file_start = next(i for i, (file_id, length) in disk_map.items() if file_id == target_file_id)
    for i in sorted(disk_map.keys()):
        if i > file_start:
            break
        if disk_map[i][0] is None and disk_map[i][1] >= disk_map[file_start][1]:
            remaining_space = disk_map[i][1] - disk_map[file_start][1]
            disk_map[i] = disk_map[file_start]
            disk_map[file_start] = (None, disk_map[file_start][1])
            if remaining_space > 0:
                disk_map[i+disk_map[i][1]] = (None, remaining_space)
            break


def defrag(disk_map):
    max_file_id = disk_map[max(disk_map.keys())][0]
    for target_file_id in range(max_file_id, 0, -1):
        defrag_file(disk_map, target_file_id)

    contents = []
    for i in sorted(disk_map.keys()):
        contents.extend([disk_map[i][0]] * disk_map[i][1])
    return contents


with open("input.txt") as input_file:
    INPUT = list(map(int, input_file.read().strip()))


# TEST_INPUT = list(map(int, "2333133121414131402"))
# print(checksum(defrag(build_disk_map(TEST_INPUT))))

print(f"Part One: {checksum(compact(build_disk_layout(INPUT)))}")
print(f"Part Two: {checksum(defrag(build_disk_map(INPUT)))}")

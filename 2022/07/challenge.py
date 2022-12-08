#!/usr/bin/env python3

from collections import namedtuple
from typing import NamedTuple

File = namedtuple("File", "name size")


class Dir(NamedTuple):
    name: str
    children: list
    parent: namedtuple

    @property
    def size(self):
        return sum(child.size for child in self.children)


def parse_input(lines):
    root = Dir("/", [], None)
    pwd = root
    for line in lines:
        line = line.strip()
        if line == "$ ls":
            continue
        elif line.startswith("$ cd"):
            path = line[5:]
            if path == "/":
                pwd = root
            elif path == "..":
                pwd = pwd.parent
            else:
                pwd = next(child for child in pwd.children if child.name == path)
        elif line.startswith("dir"):
            name = line[4:]
            pwd.children.append(Dir(name, [], pwd))
        else:
            size, filename = line.split()
            pwd.children.append(File(filename, int(size)))
    return root


def get_dir_sizes(dir):
    for child in dir.children:
        if not isinstance(child, Dir):
            continue
        yield child.size
        yield from get_dir_sizes(child)


with open("input.txt") as input_file:
    ROOT_DIR = parse_input(input_file.readlines())
    SUBDIR_SIZES = list(sorted(get_dir_sizes(ROOT_DIR)))

print(f"Part One: {sum(size for size in SUBDIR_SIZES if size <= 100000)}")
FREE_SPACE = 70000000 - ROOT_DIR.size
SPACE_NEEDED = 30000000 - FREE_SPACE
print(f"Part Two: {next(size for size in SUBDIR_SIZES if size >= SPACE_NEEDED)}")

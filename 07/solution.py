# fmt: off
import sys
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint

sys.path.append("..")


# fmt: on

@dataclass
class DirNode:
    name: str
    children: field(default_factory=list)

    @property
    def size(self):
        return sum(child.size for child in self.children)


@dataclass
class FileNode:
    name: str
    size: int


def part_1(data):
    filesystem = {}

    key = Path("/")
    while data and (line := data.pop(0)):
        if line.startswith("$ cd "):
            arg = line[5:]
            key = (key / arg).resolve()

            filesystem.setdefault(key, DirNode(arg, []))

        elif line == "$ ls":

            while data and (line := data.pop(0)):
                if line.startswith("$"):
                    data.insert(0, line)
                    break

                if line.startswith("dir"):
                    _, name = line.split()

                    dir_node = DirNode(name, [])

                    filesystem[key].children.append(dir_node)
                    dir_key = (key / name).resolve()
                    filesystem.setdefault(dir_key, dir_node)

                else:
                    size, name = line.split()
                    filesystem[key].children.append(FileNode(name, int(size)))

    s = 0
    for dir in filesystem.values():
        if dir.size < 100000:
            s += dir.size
    return s


def part_2(data):
    filesystem = {}

    key = Path("/")
    while data and (line := data.pop(0)):
        if line.startswith("$ cd "):
            arg = line[5:]
            key = (key / arg).resolve()

            filesystem.setdefault(key, DirNode(arg, []))

        elif line == "$ ls":

            while data and (line := data.pop(0)):
                if line.startswith("$"):
                    data.insert(0, line)
                    break

                if line.startswith("dir"):
                    _, name = line.split()

                    dir_node = DirNode(name, [])

                    filesystem[key].children.append(dir_node)
                    dir_key = (key / name).resolve()
                    filesystem.setdefault(dir_key, dir_node)

                else:
                    size, name = line.split()
                    filesystem[key].children.append(FileNode(name, int(size)))

    free_space = 70000000 - filesystem[Path("/")].size

    to_delete = filesystem[Path("/")].size
    print("Required:", free_space)

    required_space = 30000000 - free_space

    for dir in filesystem.values():
        if to_delete > dir.size >= required_space:
            print(f"chose {dir}")
            to_delete = dir.size

    assert to_delete != 50216456

    return to_delete


def parse(lines):
    # lines = [int(l) for l in lines]
    return lines


def main(puzzle_input_f):
    lines = [l.strip() for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(parse(lines[:])))
    print("Part 2: ", part_2(parse(lines[:])))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)

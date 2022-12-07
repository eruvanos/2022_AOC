# fmt: off
import sys
from itertools import count

sys.path.append("..")


# fmt: on

def part_1(data):
    line = data[0]

    for i in range(0, len(line)):
        if len(set(line[i: i + 4])) == 4:
            print(line[i: i + 4])
            break

    return i + 4


def part_2(data):
    line = data[0]

    for i in range(0, len(line)):
        if len(set(line[i: i + 14])) == 14:
            print(line[i: i + 14])
            break

    return i + 14


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

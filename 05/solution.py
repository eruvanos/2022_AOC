# fmt: off
import re
import sys
from typing import List

sys.path.append("..")

# fmt: on

CMD_PATTERN = re.compile("move (\d+) from (\d+) to (\d+)")


def part_1(data):
    # CrateMover 9000
    stacks, commands = data

    for command in commands:
        groups = CMD_PATTERN.match(command).groups()
        amount, source, target = map(int, groups)

        print(command)
        for _ in range(amount):
            cargo = stacks[source - 1].pop(0)
            stacks[target - 1].insert(0, cargo)

    return "".join(stack[0] for stack in stacks)


def part_2(data):
    # CrateMover 9001
    stacks, commands = data

    for command in commands:
        groups = CMD_PATTERN.match(command).groups()
        amount, source, target = map(int, groups)

        print(command)
        for i in range(amount):
            cargo = stacks[source - 1].pop(0)
            stacks[target - 1].insert(i, cargo)

    return "".join(stack[0] for stack in stacks)


def parse(lines):
    amount_of_stacks = (len(lines[0]) + 1) // 4
    stacks = [[] for _ in range(amount_of_stacks)]

    while line := lines.pop(0):
        if line.startswith(" 1 "):
            continue

        for stack in stacks:
            cargo, line = line[:4], line[4:]
            if cargo.strip():
                stack.append(cargo[1:2])

    return stacks, lines


def main(puzzle_input_f):
    lines = [l.strip("\n") for l in puzzle_input_f.readlines() if l]
    print("Part 1: ", part_1(parse(lines[:])))
    print("Part 2: ", part_2(parse(lines[:])))


if __name__ == "__main__":
    import os
    from aocpy import input_cli

    base_dir = os.path.dirname(__file__)
    with input_cli(base_dir) as f:
        main(f)

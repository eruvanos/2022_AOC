# fmt: off
import sys

sys.path.append("..")


# fmt: on

def part_1(data):

    result = 0
    elf = 0
    for line in data:
        if line == "":
            result = max(elf, result)
            elf = 0
            continue

        elf += int(line)

    return result




def part_2(data):
    result = 0
    elves = []
    elf = 0
    for line in data:
        if line == "":
            elves.append(elf)
            elf = 0
            continue

        elf += int(line)



    return sum(list(sorted(elves))[-3:])


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

    base_dir = os.path.dirname  (__file__)
    with input_cli(base_dir) as f:
        main(f)

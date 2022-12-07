# fmt: off
import sys

sys.path.append("..")


# fmt: on

order = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def part_1(data):
    lines = [
        (l[:len(l) // 2], l[len(l) // 2:])
        for l in data
    ]


    res = 0
    for x, y in lines:

        c = (set(x) & set(y)).pop()
        res += order.index(c)

    return res



def part_2(data):
    lines = [
        set(l)
        for l in data
    ]

    res = 0
    while lines:
        a = (lines.pop(0) & lines.pop(0) & lines.pop(0)).pop()
        res += order.index(a)

    return res



def parse(lines):
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

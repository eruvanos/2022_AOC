# fmt: off
import sys
from typing import List, Tuple

sys.path.append("..")


# fmt: on

class Range:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @staticmethod
    def parse(text: str):
        a, b = text.split("-")
        return Range(int(a), int(b))

    def subrange_of(self, other: "Range"):
        return self.a >= other.a and self.b <= other.b

    def overlap(self, other: "Range"):
        if other.a <= self.a <= other.b:
            return True

        if other.a <= self.b <= other.b:
            return True

        if self.a <= other.a <= self.b:
            return True

        if self.a <= other.b <= self.b:
            return True

        return False

    def __str__(self):
        return f"[{self.a}-{self.b}]"


def part_1(data: List[Tuple[Range, Range]]):
    counter = 0
    for l, r in data:

        print(l, r)

        if l.subrange_of(r) or r.subrange_of(l):
            print("   ✅")
            counter += 1



    return counter



def part_2(data):
    counter = 0
    for l, r in data:

        print(l, r)

        if l.overlap(r):
            print("   ✅")
            counter += 1

    return counter


def parse(lines):
    result = []
    for line in lines:
        l, r = line.split(",")
        result.append((Range.parse(l), Range.parse(r)))

    return result


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

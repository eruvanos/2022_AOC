# fmt: off
import sys
from ast import literal_eval
from itertools import count, zip_longest

sys.path.append("..")


# fmt: on

def compare(left, right) -> int:
    """Compare left and right.

    :return: <0 if left is smaller, >0 if left is bigger
    """
    # print(f"compare {left} < {right}")
    match left, right:
        case int(l), int(r):
            return l - r
        case list(l), list(r):
            for li, ri in zip_longest(l, r, fillvalue=None):
                if li is None:
                    return -1
                if ri is None:
                    return 1

                diff = compare(li, ri)
                if diff != 0:
                    return diff
                else:
                    continue
            return 0  # if still the same

        case int(l), list(r):
            return compare([l], r)
        case list(l), int(r):
            return compare(l, [r])


def part_1(data):
    index_sum = 0

    for i in count(1):
        # print(f"== Round {i} ==")
        left = data.pop(0)
        right = data.pop(0)

        if left < right:
            index_sum += i
            # print("\tRight order")
        else:
            # print("\tNot right order")
            pass

        if not data:
            break  # already reached end of input

    return index_sum


class Term:
    def __init__(self, term):
        self.term = term

    def __lt__(self, other: "Term"):
        return compare(self.term, other.term) < 0


def part_2(data):
    dv1 = Term([[2]])
    dv2 = Term([[6]])
    data = list(sorted(data + [dv1, dv2]))

    return (data.index(dv1) + 1) * (data.index(dv2) + 1)


def parse(lines):
    lines = [Term(literal_eval(l)) for l in lines if l]
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

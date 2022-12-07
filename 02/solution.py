# fmt: off
import sys

sys.path.append("..")

# fmt: on

A = "A"  # ROCK
B = "B"  # PAPER
C = "C"  # SCISSOR

X = "X"  # ROCK
Y = "Y"  # PAPER
Z = "Z"  # SCISSOR

SCORE_OUTCOME_1 = {
    (A, X): 1 + 3,
    (A, Y): 2 + 6,
    (A, Z): 3 + 0,

    (B, X): 1 + 0,
    (B, Y): 2 + 3,
    (B, Z): 3 + 6,

    (C, X): 1 + 6,
    (C, Y): 2 + 0,
    (C, Z): 3 + 3,
}


def part_1(data):
    score = 0
    for elf, me in data:
        score += SCORE_OUTCOME_1[(elf, me)]

    return score


SCORE_OUTCOME_2 = {
    (A, X): 0+3,
    (A, Y): 3+1,
    (A, Z): 6+2,

    (B, X): 0+1,
    (B, Y): 3+2,
    (B, Z): 6+3,

    (C, X): 0+2,
    (C, Y): 3+3,
    (C, Z): 6+1,
}



def part_2(data):
    score = 0
    for elf, me in data:
        score += SCORE_OUTCOME_2[(elf, me)]

    return score


def parse(lines):
    lines = [l.split() for l in lines]
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

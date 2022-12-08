# fmt: off
import sys

from utils.vector import Vec2

sys.path.append("..")


# fmt: on

def part_1(data):
    visible = set()

    # left-right
    for y in range(len(data)):
        shadow = -1
        for x in range(len(data)):
            t = data[y][x]
            if t > shadow:
                visible.add((x, y))
                # print(f"left-right {(x, y)}")
                shadow = t

    # right-left
    for y in range(len(data)):
        shadow = -1
        for x in range(len(data)):
            x = len(data) - x - 1
            t = data[y][x]
            if t > shadow:
                visible.add((x, y))
                # print(f"right-left {(x, y)}")
                shadow = t

    # top-bottom
    for x in range(len(data)):
        shadow = -1
        for y in range(len(data)):
            t = data[y][x]
            if t > shadow:
                visible.add((x, y))
                # print(f"top-bottom{(x, y)}")
                shadow = t

    # bottom-top
    for x in range(len(data)):
        shadow = -1
        for y in range(len(data)):
            y = len(data) - y - 1
            t = data[y][x]
            if t > shadow:
                visible.add((x, y))
                # print(f"bottom-top {(x, y)}")
                shadow = t

    return len(visible)


def calc_score(data, start: Vec2):
    height = data[start.y][start.x]

    score = 1
    for dir_vec in [
        Vec2(0, 1),  # down
        Vec2(0, -1),  # up
        Vec2(1, 0),  # right
        Vec2(-1, 0),  # left
    ]:

        count = 0
        for off in range(1, len(data)):
            x, y = start + dir_vec * off

            if 0 <= y < len(data) and 0 <= x < len(data):
                t = data[y][x]
                if t < height:
                    count += 1
                else:
                    count += 1
                    break
            else:
                break

        # print(f"{dir_vec=}: {count}")
        score *= count

    return score


def part_2(data):
    # look down
    score = 0
    for x in range(len(data)):
        for y in range(len(data)):
            new_score = calc_score(data, Vec2(x, y))
            # print(f"{x,y}: {new_score}")
            score = max(score, new_score)

    return score


def parse(lines):
    lines = [[int(l) for l in row] for row in lines]
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

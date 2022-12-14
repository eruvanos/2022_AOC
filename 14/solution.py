# fmt: off
import sys
from itertools import cycle
from typing import List

from utils.path import MapGraph
from utils.vector import Vec2

sys.path.append("..")


# fmt: on

def part_1(data: List[List[Vec2]]):
    world = MapGraph({})

    for rock in data:
        pos = rock[0]
        for target in rock[1:]:
            if pos.x == target.x:
                x_range = cycle([pos.x])
                y_range = range(min(pos.y, target.y), max(pos.y, target.y) + 1)
            if pos.y == target.y:
                x_range = range(min(pos.x, target.x), max(pos.x, target.x) + 1)
                y_range = cycle([pos.y])

            for x, y in zip(x_range, y_range):
                world[Vec2(x, y)] = "#"

            pos = target

    # print(world.max_y)
    # print(world)

    sand_amount = 0

    while True:
        sand = Vec2(500, 0)
        while True:
            if world.get(sand + (0, 1)) is None:
                sand = sand + (0, 1)
            elif world.get(sand + (-1, 1)) is None:
                sand = sand + (-1, 1)
            elif world.get(sand + (1, 1)) is None:
                sand = sand + (1, 1)
            else:
                world[sand] = "o"
                sand_amount += 1
                break  # sand stops here

            if sand.y > world.max_y:
                break  # sand goes to void!

        if sand.y > world.max_y:
            break  # sand goes to void!

    return sand_amount

def part_2(data):
    world = MapGraph({})

    for rock in data:
        pos = rock[0]
        for target in rock[1:]:
            if pos.x == target.x:
                x_range = cycle([pos.x])
                y_range = range(min(pos.y, target.y), max(pos.y, target.y) + 1)
            if pos.y == target.y:
                x_range = range(min(pos.x, target.x), max(pos.x, target.x) + 1)
                y_range = cycle([pos.y])

            for x, y in zip(x_range, y_range):
                world[Vec2(x, y)] = "#"

            pos = target

    # print(world.max_y)
    # print(world)

    sand_amount = 0
    floor = world.max_y

    while True:
        sand = Vec2(500, 0)
        while True:
            if world.get(sand + (0, 1)) is None:
                sand = sand + (0, 1)
            elif world.get(sand + (-1, 1)) is None:
                sand = sand + (-1, 1)
            elif world.get(sand + (1, 1)) is None:
                sand = sand + (1, 1)
            else:
                world[sand] = "o"
                sand_amount += 1
                break  # sand stops here

            if sand.y > floor:
                world[sand] = "o"
                sand_amount += 1
                break  # sand stops on floor

        if sand == Vec2(500, 0):
            break  # sand source blocked

    # print(world)

    return sand_amount


# 498,4 -> 498,6 -> 496,6
# 503,4 -> 502,4 -> 502,9 -> 494,9
def parse(lines):
    lines = [list(map(Vec2.from_string, l.split(" -> "))) for l in lines]
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

# fmt: off
import re
import sys
from queue import PriorityQueue
from typing import NamedTuple

from utils.path import MapGraph, manhattan
from utils.vector import Vec2, manhattan_neighbors

sys.path.append("..")


# fmt: on

class SensorMsg(NamedTuple):
    sensor: Vec2
    beacon: Vec2


def fields_in_range(center, radius):
    result = set()

    tasks = PriorityQueue()
    discovered = set()
    tasks.put((0, center))

    while not tasks.empty():
        distance, cur = tasks.get()

        if distance <= radius:
            result.add(cur)

            for n in manhattan_neighbors(cur):
                if n not in discovered:
                    discovered.add(n)
                    tasks.put((distance + 1, n))

    return result


def part_1(data: list[SensorMsg]):
    world = MapGraph()

    for sensor, beacon in data:
        print(sensor, manhattan(sensor, beacon))
        world[sensor] = "S"
        world[beacon] = "B"

        world.update({v: "#" for v in fields_in_range(sensor, manhattan(sensor, beacon)) if v.y == 2000000})

    print()
    print(world)

    blocked = 0
    for i in range(world.min_x, world.max_x):
        if world.get(Vec2(i, 10)) not in (None, "B"):
            blocked += 1

    return blocked


def part_2(data: list[SensorMsg]):
    pass


def parse(lines):
    pattern = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

    data = []
    for l in lines:
        sx, sy, bx, by = map(int, pattern.match(l).groups())

        data.append(SensorMsg(Vec2(sx, sy), Vec2(bx, by)))
    return data


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

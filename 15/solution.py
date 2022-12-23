# fmt: off
import re
import sys
from typing import NamedTuple, Union

from utils.path import MapGraph, manhattan
from utils.vector import Vec2

sys.path.append("..")


# fmt: on

class SensorMsg(NamedTuple):
    sensor: Vec2
    beacon: Vec2


class Range(NamedTuple):
    start: int
    end: int

    def __len__(self):
        return abs(self.end - self.start)

    def __repr__(self):
        return f"[{self.start}->{self.end}]"


    @staticmethod
    def parse(text: str):
        a, b = text.split("-")
        return Range(int(a), int(b))

    def subrange_of(self, other: "Range"):
        return self.start >= other.start and self.end <= other.end

    def __contains__(self, other: Union[int, "Range"]):
        if isinstance(other, int):
            return self.start <= other <= self.end
        else:
            return other.start >= self.start and other.end <= self.end


    def overlap(self, other: "Range"):
        if other.start <= self.start <= other.end:
            return True

        if other.start <= self.end <= other.end:
            return True

        if self.start <= other.start <= self.end:
            return True

        if self.start <= other.end <= self.end:
            return True

        return False


def part_1(data: list[SensorMsg], target_row=2000000):
    world = MapGraph()

    ranges = []

    for sensor, beacon in data:
        world[sensor] = "S"
        world[beacon] = "B"

        radius = manhattan(sensor, beacon)

        diff = abs(sensor.y - target_row)

        if radius > diff:
            rd = radius - diff

            start_x = sensor.x - rd
            end_x = sensor.x + rd

            ranges.append(Range(start_x, end_x))

    ranges.sort()

    print(ranges)

    blocked = 0
    while ranges:
        cur = ranges.pop(0)
        if ranges and cur.end >= ranges[0].start:
            # touch
            ranges[0] = Range(cur.start, max(cur.end, ranges[0].end))
        else:
            blocked += len(cur)

    return blocked


def analyse_row(data: list[SensorMsg], y: int):
    ranges = []
    for sensor, beacon in data:

        radius = manhattan(sensor, beacon)

        diff = abs(sensor.y - y)

        if radius > diff:
            rd = radius - diff

            start_x = sensor.x - rd
            end_x = sensor.x + rd

            ranges.append(Range(start_x, end_x))

    return sorted(ranges)


def combine_ranges(ranges: list[Range]):
    ranges = ranges[:]
    while ranges:
        cur = ranges.pop(0)
        if ranges and cur.end >= ranges[0].start:
            # touch
            ranges[0] = Range(cur.start, max(cur.end, ranges[0].end))
        else:
            yield cur


def part_2(data: list[SensorMsg], area=4000000):
    for y in range(0, area + 1):

        ranges = analyse_row(data, y)
        ranges = list(combine_ranges(ranges))

        x = 0
        for r in ranges:
            if r.start <= x:
                x = max(x, r.end + 1)
            else:
                break

        if x <= area:
            print("free", x, y)
            break

    # assert x * 4000000 + y > 11747171442119
    # assert x * 4000000 + y < 21436616000000
    return x * 4000000 + y


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

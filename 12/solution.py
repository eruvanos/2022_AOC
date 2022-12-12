# fmt: off
import sys
from typing import List

from utils.parse import map_from_lines
from utils.path import MapGraph, a_star_search
from utils.vector import Vec2, manhattan_neighbors

sys.path.append("..")


# fmt: on


class CustomMap(MapGraph):

    def accessible(self, position: Vec2, neighbor: Vec2):
        if neighbor not in self.data:
            return False

        diff = ord(self.get(neighbor)) - ord(self.get(position))
        # if diff < -1:  # do not fall
        #     return False

        if diff > 1:  # do not climb
            return False

        return True

    def neighbors(self, current: Vec2) -> List:
        return [n for n in manhattan_neighbors(current) if self.accessible(current, n)]


def part_1(data):
    grid = CustomMap(data)

    # find start and end
    start = None
    end = None
    for pos, value in grid:
        if value == "S":
            start = pos
        if value == "E":
            end = pos

        if start and end:
            break

    grid[start] = "a"
    grid[end] = "z"

    result = a_star_search(grid, start, end)

    return len(result.path)


def part_2(data):
    grid = CustomMap(data)

    # find and elevate start and end
    start = None
    end = None
    for pos, value in grid:
        if value == "S":
            start = pos
        if value == "E":
            end = pos

        if start and end:
            break

    grid[start] = "a"
    grid[end] = "z"

    # search best start
    shortest_path = 999

    for pos, value in data.items():
        if value == "a":
            result = a_star_search(grid, pos, end)
            if result.path:
                shortest_path = min(shortest_path, len(result.path))

    return shortest_path


def parse(lines):
    return map_from_lines(lines)


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

# fmt: off
import sys
from itertools import cycle

from tqdm import tqdm

from utils.path import MapGraph
from utils.vector import Vec2

sys.path.append("..")

# fmt: on

DEBUG = True

def minus(spawn_high):
    return [Vec2(2 + x, spawn_high) for x in range(4)]


def plus(spawn_high):
    return (
        [Vec2(2 + 1, spawn_high + 2)] +
        [Vec2(2 + x, spawn_high + 1) for x in range(3)] +
        [Vec2(2 + 1, spawn_high + 0)]
    )


def l(spawn_high):
    """
    ..#
    ..#
    ###
    """
    return (
        [Vec2(2 + x, spawn_high) for x in range(3)] +
        [Vec2(2 + 2, spawn_high + 1)] +
        [Vec2(2 + 2, spawn_high + 2)]
    )


def i(spawn_high):
    """
    #
    #
    #
    #
    """
    return [Vec2(2, spawn_high + y) for y in range(4)]


def square(spawn_high):
    return [
        Vec2(2 + 0, spawn_high),
        Vec2(2 + 1, spawn_high),
        Vec2(2 + 0, spawn_high + 1),
        Vec2(2 + 1, spawn_high + 1),
    ]

def print_with_rock(graph, rock=tuple()):
    if not DEBUG:
        return

    for vec in rock:
        graph[vec] = "@"

    print()
    print(graph.to_string(y_reversed=True))
    print()

    for vec in rock:
        del graph[vec]


def part_1(data, stones_to_simulate=2022):
    forms = cycle(["-", "+", "L", "I", "S"])
    sequence = cycle(data)

    # two units free to left edge
    # three units above ground

    fall = Vec2(0, -1)
    left = Vec2(-1, 0)
    right = Vec2(1, 0)

    factories = {
        "-": minus,
        "+": plus,
        "L": l,
        "I": i,
        "S": square,
    }

    graph = MapGraph()

    for x in range(7):
        graph[Vec2(x, 0)] = "#"

    for idx, form in tqdm(enumerate(forms), total=stones_to_simulate):
        if idx == stones_to_simulate:
            break

        # spawn rock
        spawn_high = graph.max_y + 4
        rock = factories[form](spawn_high)
        # print_with_rock(graph, rock)

        for c in sequence:
            # move
            movement = left if c == "<" else right
            new_rock = [vec + movement for vec in rock]
            if all(map(lambda v: 0 <= v.x <= 6, new_rock)) and not any(graph.get(vec) for vec in new_rock):
                rock = new_rock

            # fall
            new_rock = [vec + fall for vec in rock]
            if any(graph.get(vec) for vec in new_rock):
                break

            rock = new_rock

            # show tick
            # print_with_rock(graph, rock)

        # fix rock
        for vec in rock:
            graph[vec] = "#"


        # print_with_rock(graph)

    print_with_rock(graph)
    return graph.max_y


def part_2(data):
    return part_1(data, stones_to_simulate=1000000000000)


def parse(lines):
    # lines = [int(l) for l in lines]
    return lines[0]


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

# fmt: off
import sys
from io import StringIO

from utils.directions import UDRL_VEC
from utils.vector import Vec2, neigbors

sys.path.append("..")


# fmt: on

def norm(vec: Vec2):
    return Vec2(vec.x // abs(vec.x) if vec.x else 0, vec.y // abs(vec.y) if vec.y else 0)


class Node:
    def __init__(self, *, pos=Vec2(0, 0), parent: "Node" = None):
        self.pos = pos
        self.parent = parent
        self.visited = {pos}

    def update(self):
        if not self.parent:
            return

        head = self.parent.pos
        tail = self.pos

        if tail not in neigbors(head) and tail != head:
            diff = head - tail
            self.pos += norm(diff)
            self.visited.add(self.pos)


class World:
    def __init__(self, node_count=1):
        self.head = Node()
        self.nodes = []

        cur = self.head
        for _ in range(node_count):
            cur = Node(parent=cur)

            self.tail = cur
            self.nodes.append(cur)

    def move(self, dir):
        vec = UDRL_VEC[dir]
        self.head.pos += vec

        for node in self.nodes:
            node.update()


    def __repr__(self):
        rep = StringIO()

        center_x, center_y = self.head.pos

        PADDING = 4

        for y in reversed(range(center_y - PADDING, center_y + PADDING)):
            rep.write("\n")
            for x in range(center_x - PADDING, center_x + PADDING):

                v = Vec2(x, y)
                if v == self.head:
                    c = "H"
                elif v == self.tail:
                    c = "T"
                elif v == Vec2(0, 0):
                    c = "s"
                elif v in self.tail.visited:
                    c = "#"
                else:
                    c = "."

                rep.write(c)

        return rep.getvalue()


def part_1(data):
    world = World()

    for dir, steps in map(str.split, data):
        steps = int(steps)

        for step in range(steps):
            world.move(dir)
            print(world)
            print()

    return len(world.tail.visited)


def part_2(data):
    world = World(node_count=9)

    for dir, steps in map(str.split, data):
        steps = int(steps)

        for step in range(steps):
            world.move(dir)
            print(world)
            print()

    return len(world.tail.visited)


def parse(lines):
    # lines = [int(l) for l in lines]
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

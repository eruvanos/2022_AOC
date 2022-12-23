# fmt: off
import sys
from functools import lru_cache
from queue import Queue
from typing import NamedTuple, List

from tqdm import tqdm

from utils.data import subsets_k
from utils.path import Graph, breadth_first_search

sys.path.append("..")


# fmt: on

class Entry(NamedTuple):
    name: str
    flow_rate: int
    connections_to: list[str]


class ConnectionGraph(Graph):
    def __init__(self, data: dict[str, Entry]):
        self.data = data

    def neighbors(self, current: str) -> List:
        return self.data[current].connections_to

    def cost(self, current: str, neighbor: str) -> int:
        return 1

    @lru_cache
    def find_path(self, a: str, b: str):
        return breadth_first_search(self, a, [b])

    # def pressure_released_by_path(self, combination: list[str], max_time=26):
    #     time = 0
    #     flow = 0
    #     released = 0
    #
    #     pos = "AA"
    #     for vent in combination:
    #         cost = len(self.find_path(pos, vent).path)
    #         released += flow * min(cost + 1, max_time - time)
    #         time += cost + 1
    #         flow += self.data[vent].flow_rate
    #         pos = vent
    #
    #         if time >= max_time:
    #             break
    #     else:
    #         released += flow * (max_time - time)
    #
    #     return released

    def find_max_pressure_released(self, targets: list[str], max_time=26) -> int:
        return self._find_max_pressure_released(tuple(sorted(targets)), max_time)

    @lru_cache
    def _find_max_pressure_released(self, targets: tuple[str], max_time=26) -> int:
        tasks = Queue()
        tasks.put(Task(
            time=0,
            released=0,
            pos="AA",
            flow=0,
            opened=tuple(),
            to_open=set(targets),
        ))
        max_released = 0

        while tasks.qsize():
            task = tasks.get()
            # print(task)

            # 'DD', 'BB', 'JJ', 'HH', 'EE', 'CC'
            for vent in task.to_open:
                time = task.time
                released = task.released
                # move and open vent
                cost = len(self.find_path(task.pos, vent).path) + 1
                released += task.flow * min(cost, max_time - task.time)
                flow = task.flow + self.data[vent].flow_rate
                max_released = max(max_released, released)
                time += cost
                if time >= max_time:
                    continue

                tasks.put(Task(
                    time=time,
                    pos=vent,
                    released=released,
                    flow=flow,
                    opened=task.opened + (vent,),
                    to_open=task.to_open - {vent}
                ))

            if not task.to_open:
                until_end = max_time - task.time
                released = task.released + task.flow * until_end
                max_released = max(max_released, released)

        return max_released


class Task(NamedTuple):
    time: int
    pos: str
    released: int
    flow: int
    opened: tuple
    to_open: set


def part_1(data):
    targets = list(e.name for e in data.values() if e.flow_rate > 0)

    graph = ConnectionGraph(data)
    return graph.find_max_pressure_released(targets, 30)


def part_2(data):
    targets = list(e.name for e in data.values() if e.flow_rate > 0)

    graph = ConnectionGraph(data)

    max_pressure = 0

    for me, elefant in tqdm(list(subsets_k(targets, 2))):
        pressure = graph.find_max_pressure_released(me) + graph.find_max_pressure_released(elefant)
        max_pressure = max(max_pressure, pressure)

    return max_pressure


def parse(lines):
    data = {}
    for l in lines:
        name = l[6:8]
        data[name] = Entry(
            name=name,
            flow_rate=int(l.split("=")[1].split(";")[0]),
            connections_to=[c.strip() for c in l.replace("valves", "valve").split("valve")[-1].split(",")],
        )
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

# fmt: off
import sys
from collections import defaultdict
from queue import PriorityQueue
from typing import NamedTuple, Callable

sys.path.append("..")


# fmt: on

class Entry(NamedTuple):
    name: str
    flow_rate: int
    connections_to: list[str]


class State(NamedTuple):
    time_passed: int
    opened: set[str]
    pos: str
    history: list[str]
    flow_rate: int
    released: int

    def __repr__(self):
        return f"{self.pos=}, {self.time_passed=}, opened={len(self.opened)}, {self.flow_rate=}, {self.released=}"


def solve(
    actions: Callable,
    rating: Callable,
    start_state: State
):
    finished = []
    tasks = PriorityQueue()
    tasks.put((0, start_state))

    while tasks:
        prio, state = tasks.get()
        print(f"(1/{tasks.qsize()})  process {prio}-{state}")

        if state.time_passed >= 30:
            finished.append(state)
            continue

        for ns in actions(state):
            score = rating(ns)

            if score is not None:
                print("drop state, bad score")
                tasks.put((score, ns))

    return finished


def part_1(data):

    targets = {entry.name for entry in data.values() if entry.flow_rate > 0}

    def actions(state: State) -> list[State]:
        time_passed = state.time_passed + 1
        released = state.released + state.flow_rate

        if targets == state.opened:
            yield State(
                time_passed=time_passed,
                released=released,
                opened=state.opened,
                flow_rate=state.flow_rate,
                history=state.history + [
                    f"wait, {state.flow_rate};{released=}"],
                pos=state.pos
            )
            return

        # open vent
        if state.pos not in state.opened and data[state.pos].flow_rate > 0:
            new_flow_rate = state.flow_rate + data[state.pos].flow_rate
            yield State(
                time_passed=time_passed,
                released=released,
                opened=state.opened | {state.pos},
                flow_rate=new_flow_rate,
                history=state.history + [
                    f"open {state.pos}, add {data[state.pos].flow_rate} ({new_flow_rate});{released}"],
                pos=state.pos
            )
        else:

            # only move if no valve to open
            for cn in data[state.pos].connections_to:
                yield State(
                    time_passed=time_passed,
                    released=released,
                    opened=state.opened,
                    flow_rate=state.flow_rate,
                    history=state.history + [f"move to {state.pos}, {released}"],
                    pos=cn
                )

    class Rating:
        def __init__(self):
            self.high_scores = defaultdict(int)

        def __call__(self, state: State):
            high_score = self.high_scores[state.time_passed]
            if state.released < high_score * 0.9:
                return None
            self.high_scores[state.released] = max(high_score, state.released)

            #
            # score = state.released + state.flow_rate * (30 - state.time_passed)
            return - len(state.opened)

    finished = solve(actions=actions, rating=Rating(), start_state=State(
        time_passed=0,
        opened=set(),
        pos="AA",
        history=[],
        flow_rate=0,
        released=0,
    ))

    return max(map(lambda s: s.released, finished))


def part_2(data):
    pass


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

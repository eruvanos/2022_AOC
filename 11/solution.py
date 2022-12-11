# fmt: off
import math
import sys
from dataclasses import dataclass, field
from operator import attrgetter
from typing import NamedTuple, List

sys.path.append("..")


# fmt: on


class ItemTarget(NamedTuple):
    item: int
    target: int


@dataclass
class Monkey:
    name: str
    items: field(default_factory=list)
    operation: str
    divider: int
    true_target: int
    false_target: int

    inspections = 0

    def tick(self, lcm=0) -> List[ItemTarget]:
        targets = []
        for item in self.items:
            self.inspections += 1
            new = eval(self.operation, {"old": item})

            val = new % lcm if lcm else new // 3

            target = self.true_target if val % self.divider == 0.0 else self.false_target

            # if val and val % self.divider == 0:
            #     val = self.divider

            # print(f"{self.name} {item}->{new}->{val} => {target}")
            targets.append(ItemTarget(val, target))

        self.items = []
        return targets

    def __repr__(self):
        return f"[M:{self.name}:{self.items}]"


def part_1(monkeys: List[Monkey]):
    for i in range(20):
        # print(f"Start round {i}")

        for monkey in monkeys:
            targets = monkey.tick()

            for item, target in targets:
                monkeys[target].items.append(item)

    first, second, *_ = sorted(map(attrgetter("inspections"), monkeys), reverse=True)
    return first * second


def part_2(monkeys):
    lcm = math.lcm(*(monkey.divider for monkey in monkeys))
    print("LCM", lcm)

    for i in range(10000):
        # print(f"Start round {i}")

        for monkey in monkeys:
            targets = monkey.tick(lcm=lcm)

            for item, target in targets:
                monkeys[target].items.append(item)

    first, second, *_ = sorted(map(attrgetter("inspections"), monkeys), reverse=True)
    return first * second


def parse(lines):
    monkeys = []

    while lines:
        monkeys.append(Monkey(
            name=lines.pop(0)[-2:-1],
            items=list(map(int, lines.pop(0).split(":")[1].strip().split(","))),
            operation=lines.pop(0).split("=")[1].strip(),
            divider=int(lines.pop(0)[-2:].strip()),
            true_target=int(lines.pop(0)[-1:]),
            false_target=int(lines.pop(0)[-1:]),
        ))

        if lines:
            lines.pop(0)

    return monkeys


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

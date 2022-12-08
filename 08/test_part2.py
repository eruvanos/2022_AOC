from pathlib import Path

import solution
from utils.vector import Vec2


def test_part_2():
    lines = Path("test_input.txt").read_text().splitlines()
    data = solution.parse(lines)

    result = solution.calc_score(data, Vec2(0, 2))
    assert result == 0

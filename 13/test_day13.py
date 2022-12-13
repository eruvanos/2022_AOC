from pathlib import Path

import pytest
from pytest import param

import solution

files = [
    ("test_input.txt", 13, 140),
]


@pytest.mark.parametrize(
    "file,expected",
    [param(Path(file), expected, id=file) for file, expected, _ in files],
)
def test_part_1(file: Path, expected):
    lines = file.read_text().splitlines()

    result = solution.part_1(solution.parse(lines))
    assert result == expected


@pytest.mark.parametrize(
    "file,expected",
    [param(Path(file), expected, id=file) for file, _, expected in files],
)
def test_part_2(file: Path, expected):
    lines = file.read_text().splitlines()

    result = solution.part_2(solution.parse(lines))
    assert result == expected


def test_compare_2():
    assert solution.compare([[1], [2, 3, 4]], [[1], 4]) < 0


def test_compare_3():
    assert solution.compare([9], [[8, 7, 6]]) > 0

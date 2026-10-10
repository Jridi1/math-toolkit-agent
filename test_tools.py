import pytest
from agent import add_numbers, subtract_numbers, multiply_numbers, divide_numbers


# ADD
@pytest.mark.parametrize("numbers, expected", [
    ([1, 2], 3),
    ([3, 5, 7], 15),
    ([-5, 5], 0),
    ([10, -3], 7),
    ([0.1, 0.2], 0.3),
    ([0, 0], 0),
])
def test_add(numbers, expected):
    assert add_numbers.invoke({"numbers": numbers})["result"] == pytest.approx(expected)


# SUBTRACT
@pytest.mark.parametrize("numbers, expected", [
    ([10, 3], 7),
    ([3, 10], -7),
    ([10, 3, 2], 5),
    ([-5, -5], 0),
    ([5.5, 2.5], 3.0),
])
def test_subtract(numbers, expected):
    assert subtract_numbers.invoke({"numbers": numbers})["result"] == pytest.approx(expected)


# MULTIPLY
@pytest.mark.parametrize("numbers, expected", [
    ([2, 3], 6),
    ([2, 3, 4], 24),
    ([5, 0], 0),
    ([-2, 3], -6),
    ([-2, -3], 6),
    ([0.5, 4], 2.0),
])
def test_multiply(numbers, expected):
    assert multiply_numbers.invoke({"numbers": numbers})["result"] == pytest.approx(expected)


# DIVIDE
@pytest.mark.parametrize("numbers, expected", [
    ([10, 2], 5),
    ([100, 5, 2], 10),
    ([0, 5], 0),
    ([1, 3], 1 / 3),
    ([-10, 2], -5),
])
def test_divide(numbers, expected):
    assert divide_numbers.invoke({"numbers": numbers})["result"] == pytest.approx(expected)


def test_divide_by_zero():
    result = divide_numbers.invoke({"numbers": [10, 0]})
    assert "error" in result


def test_divide_by_zero_in_middle():
    result = divide_numbers.invoke({"numbers": [10, 2, 0]})
    assert "error" in result
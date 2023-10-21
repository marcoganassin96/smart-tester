# imports
import pytest

# function to test
def sum(a: int, b: int) -> int:
    return a + b

# unit tests
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),  # positive integers
    (10, 20, 30),
    (-5, -10, -15),  # negative integers
    (-3, 7, 4),
    (0, 5, 5),  # zero as one of the inputs
    (-2, 0, -2),
    (0, 0, 0),
    (1000000, 2000000, 3000000),  # large integers
    (9999999999, 1, 10000000000),
    (2.5, 3.7, 6.2),  # floating-point numbers
    (-1.5, 2.3, 0.8),
])
def test_sum(a, b, expected):
    assert sum(a, b) == expected

@pytest.mark.parametrize("a, b", [
    ("2", 3),  # non-numeric inputs
    (2, "3"),
])
def test_sum_with_non_numeric_inputs(a, b):
    with pytest.raises(TypeError):
        sum(a, b)
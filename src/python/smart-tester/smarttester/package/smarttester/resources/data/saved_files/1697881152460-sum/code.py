# imports
import pytest

# function to test
def sum(a: int, b: int) -> int:
    return a + b

# unit tests
@pytest.mark.parametrize("a, b, expected_result", [
    (5, 10, 15),                     # Positive integers
    (-5, -10, -15),                  # Negative integers
    (0, 0, 0),                       # Zero
    (1000000, 2000000, 3000000),     # Large integers
    (0, 10, 10),                     # One input is zero
    (-1000000, 500000, -500000),     # One input is a large negative number
    (1000000, 500000, 1500000),      # One input is a large positive number
])
def test_sum(a, b, expected_result):
    # Assert that the actual result of the sum function matches the expected result
    assert sum(a, b) == expected_result
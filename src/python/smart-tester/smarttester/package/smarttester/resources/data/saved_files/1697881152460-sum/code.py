# imports
import pytest

# function to test
def sum(a: int, b: int) -> int:
    return a + b

# unit tests
@pytest.mark.parametrize("a, b, expected_result", [
    # Test the function's behavior for a wide range of possible inputs
    (5, 10, 15),  # Positive integers
    (-5, -10, -15),  # Negative integers
    (0, 0, 0),  # Zero
    (1000000, 2000000, 3000000),  # Large integers
    
    # Test edge cases that the author may not have foreseen
    (0, 10, 10),  # One of the inputs is zero
    (-1000000, 500000, -500000),  # One of the inputs is a large negative number
    (1000000, 500000, 1500000),  # One of the inputs is a large positive number
])
def test_sum(a, b, expected_result):
    # Call the function and check if the actual result matches the expected result
    assert sum(a, b) == expected_result
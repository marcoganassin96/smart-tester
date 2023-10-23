# imports
import pytest

# function to test
def sum(a: int, b: int) -> int:
    return a + b

# unit tests
@pytest.mark.parametrize(
    "a, b, expected_result", 
    [
        # Positive numbers
        (3, 5, 8),
        (10, 20, 30),
        # Negative numbers
        (-3, -5, -8),
        (-10, -20, -30),
        # Zero
        (0, 0, 0),
        (0, 10, 10),
        # Mixed positive and negative numbers
        (-3, 5, 2),
        (10, -20, -10),
        # Large numbers
        (1000000, 2000000, 3000000),
        (999999999, 1, 1000000000),
        # One of the inputs is not an integer
        pytest.param(3, 5.5, marks=pytest.mark.raises(exception=TypeError)),
        pytest.param(10, "20", marks=pytest.mark.raises(exception=TypeError)),
        # Missing one or both inputs
        pytest.param(3, marks=pytest.mark.raises(exception=TypeError)),
        pytest.param(b=5, marks=pytest.mark.raises(exception=TypeError)),
    ]
)
def test_sum(a, b, expected_result):
    assert sum(a, b) == expected_result
# imports
import pytest

# function to test
def sum(a: int, b: int) -> int:
    return a + b

# unit tests
@pytest.mark.parametrize("a, b, expected", [
    # Basic scenarios
    (2, 3, 5),
    (10, 20, 30),
    (-5, -10, -15),
    (-100, -200, -300),
    (5, -10, -5),
    (100, -200, -100),
    (-5, 10, 5),
    (-100, 200, 100),
    (0, 0, 0),
    (0, -5, -5),
    # Edge cases
    (1000000, 2000000, 3000000),
    (-1000000, -2000000, -3000000),
    (None, 5, pytest.raises(TypeError)),
    (10, None, pytest.raises(TypeError)),
    (None, None, pytest.raises(TypeError)),
    (3.14, 5, pytest.raises(TypeError)),
    (10, "20", pytest.raises(TypeError)),
    ("hello", "world", pytest.raises(TypeError)),
    # Special cases
    (5, 5, 10),
    (-10, -10, -20),
    (1000000000000000000000000, 1, 1000000000000000000000001),
    (-999999999999999999999999, 1000000000000000000000000, 1)
])
def test_sum(a, b, expected):
    if isinstance(expected, int):
        assert sum(a, b) == expected
    else:
        with expected:
            sum(a, b)
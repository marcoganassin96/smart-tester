# imports
import pytest

# function to test
def sum(a: int, b: int) -> int:
    return a + b

# unit tests
@pytest.mark.parametrize("a, b, expected", [
    (3, 5, 8),  # positive integers
    (10, 20, 30),
    (-3, -5, -8),  # negative integers
    (-10, -20, -30),
    (0, 5, 5),  # zero
    (10, 0, 10),
    (0, 0, 0),
    (1000000, 2000000, 3000000),  # large integers
    (999999999, 1, 1000000000),
    (5, None, TypeError),  # missing argument
    (None, None, TypeError),
    (3.5, 2, TypeError),  # non-integer argument
    ("hello", 5, TypeError),
    (9223372036854775807, 1, 9223372036854775808),  # large integers exceeding maximum value
    (999999999999999999999999, 1, 1000000000000000000000000),
    (-9223372036854775808, -1, -9223372036854775809),  # small integers exceeding minimum value
    (-999999999999999999999999, -1, -1000000000000000000000000),
    (9223372036854775807, 2, OverflowError),  # sum exceeding maximum value
    (-9223372036854775808, -2, OverflowError),  # sum below minimum value
    (3, 2.5, TypeError),  # sum resulting in float
    (2.5, 3.5, TypeError)
])
def test_sum(a, b, expected):
    if expected == TypeError:
        with pytest.raises(TypeError):
            sum(a, b)
    elif expected == OverflowError:
        with pytest.raises(OverflowError):
            sum(a, b)
    else:
        assert sum(a, b) == expected
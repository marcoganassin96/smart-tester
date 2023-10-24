# imports
import pytest

# function to test
def sum(a: int, b: int) -> int:
    return a + b

# unit tests
@pytest.mark.parametrize("a, b, expected", [
    # Basic scenarios
    (3, 4, 7),
    (5, 0, 5),
    (-2, -3, -5),
    # Large numbers
    (1000000, 2000000, 3000000),
    (999999, 0, 999999),
    (-1000000, -2000000, -3000000),
    # Edge cases
    (0, 0, 0),
    (5, -5, 0),
    (-7, 7, 0),
    # Type checking
    pytest.param(3.5, 4.2, None, marks=pytest.mark.xfail(raises=TypeError)),
    pytest.param("2", 3, None, marks=pytest.mark.xfail(raises=TypeError)),
    # Overflow
    pytest.param(2**31, 2**31, None, marks=pytest.mark.xfail(raises=OverflowError)),
    pytest.param(-2**31, -2**31, None, marks=pytest.mark.xfail(raises=OverflowError)),
    # Different integer types
    (5, 3, 8),
    (5, 3, 8),
    # Non-integer inputs
    pytest.param(3.5, 4.2, None, marks=pytest.mark.xfail(raises=TypeError)),
    pytest.param("2", 3.5, None, marks=pytest.mark.xfail(raises=TypeError)),
    # Unusual numeric representations
    ("0x10", "0x20", 48),
    ("0b101", "0b110", 11),
])
def test_sum(a, b, expected):
    assert sum(a, b) == expected
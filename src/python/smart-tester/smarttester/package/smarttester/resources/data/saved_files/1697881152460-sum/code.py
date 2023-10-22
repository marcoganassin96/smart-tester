# imports
import pytest

# function to test
def sum(a: int, b: int) -> int:
    return a + b

# unit tests
@pytest.mark.parametrize("a, b, expected_result", [
    # Test cases for a wide range of possible inputs
    (5, 10, 15),                    # Positive integers
    (-5, -10, -15),                 # Negative integers
    (0, 0, 0),                      # Zero
    (1000000, 2000000, 3000000),    # Large integers
    
    # Test cases for edge cases
    (0, 10, 10),                    # One input is zero
    (-1000000, 500000, -500000),    # One input is a large negative number
    (1000000, 500000, 1500000),     # One input is a large positive number
    
    # Test cases for non-integer inputs
    (3.14, 2.5, TypeError),          # Floating-point numbers
    ("10", "20", TypeError),         # Strings
    (None, 5, TypeError),            # None values
    
    # Test cases for integer overflow
    (10000000000000000000, 20000000000000000000, OverflowError),  # Large positive integers
    (-10000000000000000000, -20000000000000000000, OverflowError),  # Large negative integers
    
    # Test cases for invalid argument types
    (TypeError, 5, TypeError),       # Missing arguments
    (10, 20, 30, TypeError),         # Extra arguments
    
    # Test cases for unexpected behavior
    ("abc", "def", TypeError),       # Non-numeric inputs
    (10, "20", TypeError),           # Mixed numeric and non-numeric inputs
    (10, 3.14, TypeError),           # Inputs of different types
    
    # Test cases for special integer values
    (0, -0, 0),                      # Zero and negative zero
    (float('inf'), float('-inf'), TypeError)  # Infinity
])
def test_sum(a, b, expected_result):
    if expected_result == TypeError:
        with pytest.raises(TypeError):
            sum(a, b)
    else:
        assert sum(a, b) == expected_result
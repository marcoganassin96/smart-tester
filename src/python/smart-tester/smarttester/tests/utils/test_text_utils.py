# imports
import pytest
from smarttester.utils.text_utils import _get_bullets_number

# unit tests
# below, each test case is represented by a tuple passed to the @pytest.mark.parametrize decorator

# MANUALLY FIXED: Smart Tester was not able to understand that different bullet characters must be counted as
# different bullets
@pytest.mark.parametrize(
    "text, expected",
    [
        ("", 0),  # Empty string
        ("This is a regular text without bullets.", 0),  # Text without bullets
        ("• Bullet 1\n• Bullet 2\n• Bullet 3", 3),  # Single bullet format
        ("• Bullet 1\n- Bullet 2\n* Bullet 3\n- Bullet 4", 2),  # Multiple bullet formats
        ("• Bullet 1\n• Bullet 2\n• Bullet 3 with numbers 123", 3),  # Bullets with alphanumeric characters
        ("• Bullet 1\n• Bullet 2\n• Bullet 3 with special characters @#$", 3),  # Bullets with special characters
        ("This is a regular line.\n• Bullet 1\nThis is another regular line.\n- Bullet 2\nThis is a third regular line.", 1),  # Mixed bullet and non-bullet lines
        ("• Bullet 1\n• Bullet 1\n• Bullet 2\n• Bullet 2\n• Bullet 2", 5),  # Duplicate bullets
        ("• Bullet 1\n- Bullet 2\n* Bullet 3", 1),  # Different bullet characters
        (" • Bullet 1\n• Bullet 2 \n • Bullet 3 ", 2),  # Leading and trailing spaces in bullet lines
        ("This is a regular text without bullets.\nThis is another line.\nAnd another line.", 0),
        # Text with multiple lines but no bullets
        ("• Bullet 1\n\n• Bullet 2\n\n\n• Bullet 3", 3),  # Text with empty lines
        ("• Bullet 1 - Bullet 2 * Bullet 3", 1),  # Text with multiple bullets per line
    ]
)
def test_get_bullets_number(text: str, expected: int):
    assert _get_bullets_number(text) == expected

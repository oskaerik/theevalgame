"""Tests."""
from src import run


def test_run() -> None:
    """Test."""
    # Arrange
    code = """
a = 7
b = 3
s = a + b
"""

    # Act
    symbols = run(code)

    # Assert
    assert symbols == {"a": 7, "b": 3, "s": 10}

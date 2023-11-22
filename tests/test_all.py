"""Tests."""
from src import evaluate_objectives, run


def test_run_returns_symbols() -> None:
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


def test_evaluate_objectives_returns_correct() -> None:
    """Test."""
    # Arrange
    symbols = {"a": 7, "b": 3}
    objectives = {"a": 7, "b": 3, "s": 10}

    # Act
    result = evaluate_objectives(symbols, objectives)

    # Assert
    assert result == {"a": True, "b": True, "s": False}

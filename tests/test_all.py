"""Tests."""
from src import evaluate_objectives, get_symbols


def test_run_without_initial_symbols_returns_symbols() -> None:
    # Arrange
    code = """
a = 7
b = 3
s = a + b
"""

    # Act
    symbols = get_symbols(code)

    # Assert
    assert symbols == {"a": 7, "b": 3, "s": 10}


def test_run_with_initial_symbols_returns_symbols() -> None:
    # Arrange
    code = """
b = 3
s = a + b
"""

    # Act
    symbols = get_symbols(code, symbols={"a": 7})

    # Assert
    assert symbols == {"a": 7, "b": 3, "s": 10}


def test_evaluate_objectives_returns_result() -> None:
    # Arrange
    symbols = {"a": 7, "b": 3}
    objectives = {"a": 7, "b": 3, "s": 10}

    # Act
    result = evaluate_objectives(symbols, objectives)

    # Assert
    assert result == {"a": True, "b": True, "s": False}

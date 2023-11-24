"""Tests."""
import pytest

from src import evaluate_objectives, get_symbols


@pytest.mark.parametrize(
    ("code", "initial_symbols", "expected_symbols"),
    [
        (
            """
a = 7
b = 3
s = a + b
""",
            None,
            {"a": 7, "b": 3, "s": 10},
        ),
        (
            """
b = 3
s = a + b
     """,
            {"a": 7},
            {"a": 7, "b": 3, "s": 10},
        ),
    ],
)
def test_get_symbols_returns_symbols(
    code: str, initial_symbols: dict | None, expected_symbols: dict
) -> None:
    # Act
    symbols = get_symbols(code, symbols=initial_symbols)

    # Assert
    assert symbols == expected_symbols


def test_evaluate_objectives_returns_result() -> None:
    # Arrange
    symbols = {"a": 7, "b": 3}
    objectives = {"a": 7, "b": 3, "s": 10}

    # Act
    result = evaluate_objectives(symbols, objectives)

    # Assert
    assert result == {"a": True, "b": True, "s": False}

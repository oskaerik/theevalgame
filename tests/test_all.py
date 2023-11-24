"""Tests."""
import pytest

from src import Json, evaluate_objectives, get_ast, get_symbols, is_subtree


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


@pytest.mark.parametrize(
    ("code", "expected_ast"),
    [
        ("1", {"type": "Expr", "value": {"type": "Constant", "value": 1}}),
        (
            "1+1",
            {
                "type": "Expr",
                "value": {
                    "type": "BinOp",
                    "left": {"type": "Constant", "value": 1},
                    "op": {"type": "Add"},
                    "right": {"type": "Constant", "value": 1},
                },
            },
        ),
        (
            "print('a')",
            {
                "type": "Expr",
                "value": {
                    "type": "Call",
                    "func": {"type": "Name", "id": "print"},
                    "args": [{"type": "Constant", "value": "a"}],
                    "keywords": [],
                },
            },
        ),
    ],
)
def test_get_ast_returns_ast_dict(code: str, expected_ast: dict) -> None:
    # Act
    ast = get_ast(code)

    # Assert
    assert ast == expected_ast


@pytest.mark.parametrize(
    ("tree", "expected", "expected_result"),
    [
        ({"a": 1}, {"a": 1}, True),
    ],
)
def test_is_subtree_returns_result(
    tree: Json, expected: Json, expected_result: bool
) -> None:
    # Act
    result = is_subtree(tree, expected)

    # Assert
    assert result == expected_result

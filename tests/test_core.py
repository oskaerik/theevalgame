"""Tests."""
from typing import Any

import pytest

from src.core import Json, evaluate_code, get_ast, is_subtree


@pytest.mark.parametrize(
    ("code", "expected_result", "expected_symbols"),
    [("1", 1, {}), ("(a := 1)", 1, {"a": 1})],
)
def test_evaluate_code_returns_result_and_symbols(
    code: str, expected_result: Any, expected_symbols: dict
) -> None:
    # Act
    result, symbols = evaluate_code(code)

    # Assert
    assert result == expected_result
    assert symbols == expected_symbols


@pytest.mark.parametrize(
    ("code", "expected_ast"),
    [
        ("1", {"type": "Constant", "value": 1}),
        (
            "1+1",
            {
                "type": "BinOp",
                "left": {"type": "Constant", "value": 1},
                "op": {"type": "Add"},
                "right": {"type": "Constant", "value": 1},
            },
        ),
        (
            "print('a')",
            {
                "type": "Call",
                "func": {"type": "Name", "id": "print"},
                "args": [{"type": "Constant", "value": "a"}],
                "keywords": [],
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
        ({"a": 1}, {"b": 1}, False),
        ({"a": 1}, 1, True),
        ({"a": {"b": 1}}, {"a": {"b": 1}}, True),
        ({"a": {"b": 1}}, {"a": {"b": 1}, "c": 2}, False),
        ({"a": {"b": 1, "c": 2}}, {"a": {"b": 1}}, True),
        ({"a": {"b": 1, "c": [2]}}, {"c": [2]}, True),
        ([1, 2], 2, True),
        ({"a": {"b": {"c": 0}}}, {"a": {"c": 0}}, False),
    ],
)
def test_is_subtree_returns_result(
    tree: Json, expected: Json, expected_result: bool
) -> None:
    # Act
    result = is_subtree(tree, expected)

    # Assert
    assert result == expected_result

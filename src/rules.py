"""All things rules."""
from typing import Any

from src.core import evaluate_code, get_ast, is_subtree


def rule_42(result: Any, _symbols: dict, _ast: dict) -> bool:
    """Expression should evaluate to 42."""
    return result == 42


def rule_add(_result: Any, _symbols: dict, ast: dict) -> bool:
    """Expression should contain addition."""
    return is_subtree(ast, {"op": {"type": "Add"}})


def rule_print(_result: Any, _symbols: dict, ast: dict) -> bool:
    """Expression should call print("here2!")."""
    return is_subtree(
        ast,
        {
            "type": "Call",
            "func": {"id": "print"},
            "args": [{"type": "Constant", "value": "here2!"}],
        },
    )


rules = [
    ("Your expression should evaluate to 42", rule_42),
    ("Your expression should contain an addition", rule_add),
    (
        'Time for some debugging, make sure your expression calls print("here2!")',
        rule_print,
    ),
]


def evaluate_rules(code: str) -> list:
    """Evaluate all rules."""
    result, symbols = evaluate_code(code)
    ast = get_ast(code)
    return [(rule_text, rule(result, symbols, ast)) for rule_text, rule in rules]

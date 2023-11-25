"""All things rules."""

from src.core import evaluate_code, get_ast, is_subtree


def rule_42(code: str) -> bool:
    """Expression should evaluate to 42."""
    result, _symbols = evaluate_code(code)
    return result == 42


def rule_add(code: str) -> bool:
    """Expression should contain addition."""
    ast = get_ast(code)
    return is_subtree(ast, {"op": {"type": "Add"}})


def rule_print(code: str) -> bool:
    """Expression should call print("here2!")."""
    ast = get_ast(code)
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
    return [(rule_text, rule(code)) for rule_text, rule in rules]

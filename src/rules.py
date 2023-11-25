"""All things rules."""
from typing import NamedTuple, Self

from src.core import evaluate_code, get_ast, is_subtree


class Rule(NamedTuple):
    """A rule."""

    text: str
    ok: bool


class RuleEvaluator:
    """A rule evaluator."""

    def __init__(self: Self, code: str) -> None:
        """Evaluate rules."""
        self.code = code
        self.result, self.symbols = evaluate_code(self.code)
        self.ast = get_ast(self.code)

        self.rules = [
            Rule("Your expression should evaluate to 42", self.rule_42()),
            Rule("Your expression should contain an addition", self.rule_add()),
            Rule(
                "Time for some debugging, make sure your"
                ' expression calls print("here2!")',
                self.rule_print(),
            ),
        ]

    def rule_42(self: Self) -> bool:
        """Expression should evaluate to 42."""
        return self.result == 42

    def rule_add(self: Self) -> bool:
        """Expression should contain addition."""
        return is_subtree(self.ast, {"op": {"type": "Add"}})

    def rule_print(self: Self) -> bool:
        """Expression should call print("here2!")."""
        return is_subtree(
            self.ast,
            {
                "type": "Call",
                "func": {"id": "print"},
                "args": [{"type": "Constant", "value": "here2!"}],
            },
        )

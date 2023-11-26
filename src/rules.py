"""All things rules."""
from pathlib import Path
from typing import NamedTuple, Self

from src.core import evaluate_code, get_ast, is_subtree

PASSWORD_FILE = Path("src/password.txt")


class Rule(NamedTuple):
    """A rule."""

    text: str
    ok: bool


class RuleEvaluator:
    """A rule evaluator."""

    def __init__(self: Self, code: str) -> None:
        """Evaluate rules."""
        # Create password file
        with PASSWORD_FILE.open("w") as f:
            f.write("abc123")

        self.code = code
        self.result, self.symbols = evaluate_code(self.code)
        self.ast = get_ast(self.code)

        self.rules = [
            Rule("Your expression should evaluate to 42", self.rule_42()),
            Rule("Your expression should contain an addition", self.rule_add()),
            Rule("Your expression should contain a comprehension", self.rule_comp()),
            Rule(
                "Time for some debugging, make sure your expression calls print",
                self.rule_print(),
            ),
            Rule(
                "That won't cut it, define your own print function",
                self.rule_def_print(),
            ),
            Rule(
                "Too many corner cases, your expression can't contain [",
                self.rule_bracket(),
            ),
            Rule(
                "This is getting messy, maybe OOP will solve it, define a class C",
                self.rule_class(),
            ),
            Rule(
                "Oops, I committed my password, please delete it",
                self.rule_delete(),
            ),
        ]

    def rule_42(self: Self) -> bool:
        """Expression should evaluate to 42."""
        return self.result == 42

    def rule_add(self: Self) -> bool:
        """Expression should contain addition."""
        return is_subtree(self.ast, {"op": {"type": "Add"}})

    def rule_comp(self: Self) -> bool:
        """Expression should contain a comprehension."""
        return is_subtree(self.ast, {"type": "comprehension"})

    def rule_print(self: Self) -> bool:
        """Expression should calls print."""
        return is_subtree(
            self.ast,
            {"type": "Call", "func": {"id": "print"}},
        )

    def rule_def_print(self: Self) -> bool:
        """Expression should define a function print."""
        try:
            return self.symbols["print"].__class__.__name__ == "function"
        except:  # noqa: E722
            return False

    def rule_bracket(self: Self) -> bool:
        """Expression should not contain [."""
        return "[" not in self.code

    def rule_class(self: Self) -> bool:
        """Expression should define class C."""
        if "C" not in self.symbols:
            return False
        return (
            type(self.symbols["C"]).__name__ == "type"
            and self.symbols["C"].__name__ == "C"
        )

    def rule_delete(self: Self) -> bool:
        """Expression should delete file."""
        return not PASSWORD_FILE.exists()

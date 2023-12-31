"""All things rules."""
from pathlib import Path
from typing import Any, NamedTuple, Self

from src.core import evaluate_code, get_ast, is_subtree

PASSWORD_FILE = Path("password.txt")


class Rule(NamedTuple):
    """A rule."""

    text: str
    ok: bool


class RuleEvaluator:
    """A rule evaluator."""

    def __init__(self: Self, code: str) -> None:
        """Evaluate rules."""
        # Create password.txt file
        if not PASSWORD_FILE.exists():
            with PASSWORD_FILE.open("w") as f:
                f.write("abc123")

        # Spy on __builtins__
        builtins = (eval("None", s := {}), s["__builtins__"])[-1]  # noqa: S307, PGH001
        builtins.pop("_", None)
        self.used_builtins = False

        class BuiltinsProxy:
            """For spying on builtins."""

            def __getitem__(_: Self, key: Any) -> Any:  # noqa: N805
                """Builtins were used."""
                self.used_builtins = True  # self is RuleEvaluator
                return builtins[key]

        self.code = code
        self.result, self.symbols = evaluate_code(
            self.code, {"__builtins__": BuiltinsProxy()}
        )
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
                "That won't cut it, define your own print function in globals",
                self.rule_def_print(),
            ),
            Rule(
                "Too many corner cases, your expression can't contain [",
                self.rule_bracket(),
            ),
            Rule(
                "This is getting messy, "
                "maybe OOP will solve it, define a class C in globals",
                self.rule_class(),
            ),
            Rule(
                "Oops, I committed my password, please delete it from the filesystem",
                self.rule_delete(),
            ),
            Rule(
                "Your expression should not contain... numbers",
                self.rule_no_num(),
            ),
            Rule(
                "Sorry, no builtins",
                self.rule_builtins(),
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
        """Expression should call print."""
        return is_subtree(
            self.ast,
            {"type": "Call", "func": {"id": "print"}},
        ) or is_subtree(
            self.ast,
            {"type": "Call", "func": {"type": "NamedExpr", "target": {"id": "print"}}},
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

    def rule_no_num(self: Self) -> bool:
        """Expression should not contain numbers."""
        return not any(c.isdigit() for c in self.code)

    def rule_builtins(self: Self) -> bool:
        """Expression should not use __builtins__."""
        return not self.used_builtins

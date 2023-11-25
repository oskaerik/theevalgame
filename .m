"""All things rules."""
from collections import namedtuple
from src.core import evaluate_code, get_ast, is_subtree

Rule = namedtuple('Rule', ('text', 'func', "symbols"), defaults=(None,))

class RuleEvaluator:
    def __init__(self):
        rules = [
            Rule("Your expression should evaluate to 42", self.rule_42),
            Rule("Your expression should contain an addition", self.rule_add),
            Rule(
                'Time for some debugging, make sure your expression calls print("here2!")',
                self.rule_print,
            ),
        ]

        self.code = code
        self.result, self.symbols = evaluate_code(self.code)
        self.ast = get_ast(self.code)

    def evaluate_rules(code: str) -> list:
        """Evaluate all rules."""
        return [(rule_text, rule()) for rule_text, rule in self.rules]

    def rule_42() -> bool:
        """Expression should evaluate to 42."""
        return self.result == 42


    def rule_add() -> bool:
        """Expression should contain addition."""
        return is_subtree(self.ast, {"op": {"type": "Add"}})


    def rule_print() -> bool:
        """Expression should call print("here2!")."""
        return is_subtree(
            self.ast,
            {
                "type": "Call",
                "func": {"id": "print"},
                "args": [{"type": "Constant", "value": "here2!"}],
            },
        )

def evaluate_rules(code: str) -> list:
    """Evaluate all rules."""
    return RuleEvaluator(code).evaluate_rules()

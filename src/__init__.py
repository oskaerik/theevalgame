"""Core library."""


def evaluate_objectives(code: str, objectives: dict) -> dict:
    """Evaluate objectives."""
    symbols = run(code)
    return {
        var: (val == symbols[var]) if var in symbols else False
        for var, val in objectives.items()
    }


def run(code: str) -> dict:
    """Run code."""
    symbols = {}
    exec(code, symbols)  # noqa: S102
    del symbols["__builtins__"]
    return symbols

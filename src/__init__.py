"""Core library."""


def evaluate_objectives(symbols: dict, objectives: dict) -> dict:
    """Evaluate objectives."""
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

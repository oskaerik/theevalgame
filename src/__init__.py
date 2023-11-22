"""Core library."""


def run(code: str, symbols: dict | None = None) -> dict:
    """Run code."""
    symbols = symbols or {}
    exec(code, symbols)  # noqa: S102
    del symbols["__builtins__"]
    return symbols


def evaluate_objectives(symbols: dict, objectives: dict) -> dict:
    """Evaluate objectives."""
    return {
        var: (val == symbols[var]) if var in symbols else False
        for var, val in objectives.items()
    }

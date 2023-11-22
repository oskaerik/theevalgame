"""Core library."""


def run(code: str) -> dict:
    """Run code."""
    symbols = {}
    exec(code, symbols)  # noqa: S102
    del symbols["__builtins__"]
    return symbols

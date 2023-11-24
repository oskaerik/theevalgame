"""Core library."""
import ast

Basic = str | int | float | bool
Json = dict | list | Basic | None


def get_symbols(code: str, symbols: dict | None = None) -> dict:
    """Run code and get the symbols."""
    symbols = symbols.copy() if symbols else {}
    exec(code, symbols)  # noqa: S102
    del symbols["__builtins__"]
    return symbols


def evaluate_objectives(symbols: dict, objectives: dict) -> dict:
    """Evaluate objectives."""
    return {
        var: (val == symbols[var]) if var in symbols else False
        for var, val in objectives.items()
    }


def get_ast(code: str) -> Json:
    """Get the AST of the first  expression."""
    return ast_to_json(ast.parse(code))["body"][0]  # type: ignore


def ast_to_json(node: ast.AST | Json) -> Json:
    """Get the AST as a JSON."""
    if isinstance(node, ast.AST):
        fields = {k: ast_to_json(getattr(node, k)) for k in node._fields}
        return {"type": type(node).__name__, **fields}
    if isinstance(node, list):
        return [ast_to_json(child) for child in node]
    return node


def is_subtree(tree: Json, expected: Json) -> bool:
    """Check if expected is subtree of tree."""
    if tree == expected:
        return True
    if isinstance(tree, dict):
        if isinstance(expected, dict) and all(
            key in tree and is_subtree(tree[key], value)
            for key, value in expected.items()
        ):
            return True
        return any(is_subtree(s, expected) for s in tree.values())
    if isinstance(tree, list):
        return any(is_subtree(s, expected) for s in tree)
    return False

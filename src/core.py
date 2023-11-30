"""Core library."""
import ast
from typing import Any

Basic = str | int | float | bool
Json = dict | list | Basic | None


def evaluate_code(code: str, symbols: dict | None = None) -> tuple[Any, dict]:
    """Run code and get the result and symbols."""
    symbols = symbols.copy() if symbols else {}
    result = eval(code, symbols)  # noqa: S307,PGH001
    symbols.pop("__builtins__", None)
    return result, symbols


def get_ast(code: str) -> dict:
    """Get the AST of the first expression."""
    return ast_to_json(ast.parse(code))["body"][0]["value"]  # type: ignore


def ast_to_json(node: ast.AST | Json) -> Json:
    """Get the AST as a JSON."""
    if isinstance(node, ast.AST):
        fields = {k: ast_to_json(getattr(node, k)) for k in node._fields}
        fields.pop("kind", None)
        fields.pop("ctx", None)
        return {"type": type(node).__name__, **fields}
    if isinstance(node, list):
        return [ast_to_json(child) for child in node]
    return node


def is_subtree(tree: Json, expected: Json, depth: bool = True) -> bool:
    """Check if expected is subtree of tree."""
    if tree == expected:
        return True
    if isinstance(tree, dict):
        if isinstance(expected, dict) and all(
            key in tree and is_subtree(tree[key], value, depth=False)
            for key, value in expected.items()
        ):
            return True
        return any(is_subtree(s, expected) for s in tree.values()) if depth else False
    if isinstance(tree, list):
        return any(is_subtree(s, expected) for s in tree) if depth else False
    return False

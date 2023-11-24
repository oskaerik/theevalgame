"""Code game."""
import json
from typing import Any
from uuid import uuid4

import flet as ft

from src import Json, get_ast, get_symbols, is_subtree

session_id = f"_{uuid4().hex}"


def rule_42(_ast: Json, symbols: dict) -> bool:
    """Expression should evaluate to 42."""
    return symbols.get(session_id) == 42


def rule_add(ast: Json, _symbols: dict) -> bool:
    """Expression should contain addition."""
    return is_subtree(ast, {"op": {"type": "Add"}})


def rule_print(ast: Json, _symbols: dict) -> bool:
    """Expression should call print("here2!")."""
    return is_subtree(
        ast,
        {
            "type": "Call",
            "func": {"id": "print"},
            "args": [{"type": "Constant", "value": "here2!"}],
        },
    )


rules = [
    ("Your expression should evaluate to 42", rule_42),
    ("Your expression should contain an addition", rule_add),
    (
        'Time for some debugging, make sure your expression calls print("here2!")',
        rule_print,
    ),
]


def get_banned_chars(code: str, banned: str = ";\n\r") -> set:
    """Check if code contains banned character."""
    return {char for char in code if char in banned}


def main(page: ft.Page) -> None:
    """Run flet."""

    def update_text(new_text: str) -> None:
        text_field.value = new_text
        page.update()

    def on_code_change(event: Any = None) -> None:  # noqa: ANN401
        code = (event.control.value.strip() if event else "") or "None"

        if banned := get_banned_chars(code):
            update_text(f"{next(iter(banned))} is banned, sorry")
            return

        try:
            symbols = get_symbols(f"{session_id} = {code}")
            ast = get_ast(code)

            status = ""
            for i, (rule_text, rule) in enumerate(rules):
                ok = rule(ast, symbols)
                status += f"{ok} Rule {i}: {rule_text}\n"
            update_text(
                f"""{status}

Your expression evaluates to: {symbols[session_id]}

{symbols}

{json.dumps(ast, indent=2)}"""
            )
        except Exception as e:  # noqa: BLE001
            update_text(repr(e))

    page.title = "pyquest"
    page.scroll = "adaptive"  # type: ignore

    code_field = ft.TextField(label="Write your Python here", on_change=on_code_change)
    text_field = ft.Text()

    page.add(ft.Text("pyquest"), code_field, text_field)
    on_code_change()


ft.app(port=51111, target=main, view=ft.AppView.WEB_BROWSER)

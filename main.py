"""Code game."""
import json
from typing import Any
from uuid import uuid4

import flet as ft

from src import Json, get_ast, get_symbols, is_subtree

game_id = f"game_{uuid4().hex}"


def rule_42(_ast: Json, symbols: dict) -> bool:
    """Expression should evaluate to 42."""
    return symbols.get(game_id) == 42


def rule_add(ast: Json, _symbols: dict) -> bool:
    """Expression should contain addition."""
    return is_subtree(ast, {"op": {"type": "Add"}})


rules = [
    ("Your expression should evaluate to 42", rule_42),
    ("Your expression should contain an addition", rule_add),
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
        code = (event.control.value.strip() or "") or "0"

        if banned := get_banned_chars(code):
            update_text(f"{next(iter(banned))} is banned, sorry")

        try:
            symbols = get_symbols(f"{game_id} = {code}")
            ast = get_ast(code)

            status = "Congratulations, you've beaten the game!"
            for i, (rule_text, rule) in enumerate(rules):
                if not rule(ast, symbols):
                    status = f"Rule {i}: {rule_text}"
                    break
            update_text(f"{status}\n\n{symbols}\n\n{json.dumps(ast, indent=2)}")
        except Exception as e:  # noqa: BLE001
            update_text(repr(e))

    page.title = "The PyGolf Game"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    code_field = ft.TextField(label="Python goes here", on_change=on_code_change)
    text_field = ft.Text()

    page.add(code_field, text_field)
    on_code_change()


ft.app(port=51111, target=main, view=ft.AppView.WEB_BROWSER)

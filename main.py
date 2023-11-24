"""Code game."""
import json
from typing import Any

import flet as ft

from src.core import evaluate_code, get_ast
from src.rules import evaluate_rules

title = "the eval game"


def main(page: ft.Page) -> None:
    """Run flet."""

    def update_text(new_text: str) -> None:
        text_field.value = new_text
        page.update()

    def on_code_change(event: Any = None) -> None:
        code = (event.control.value.strip() if event else "") or "None"

        try:
            status = ""
            for i, (rule_text, rule_ok) in enumerate(evaluate_rules(code)):
                status += f"{rule_ok} Rule {i}: {rule_text}\n"
            result, symbols = evaluate_code(code)
            ast = get_ast(code)
            update_text(
                f"""{status}

Your expression evaluates to: {result}

{symbols}

{json.dumps(ast, indent=2)}"""
            )
        except Exception as e:  # noqa: BLE001
            update_text(repr(e))

    page.title = title
    page.scroll = "adaptive"  # type: ignore

    code_field = ft.TextField(label="Write your Python here", on_change=on_code_change)
    text_field = ft.Text()

    page.add(ft.Text(title), code_field, text_field)
    on_code_change()


ft.app(port=51111, target=main, view=ft.AppView.WEB_BROWSER)

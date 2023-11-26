"""Code game."""
import json
from importlib import reload
from typing import Any

import flet as ft

import src.rules

title = "the eval game"


def main(page: ft.Page) -> None:
    """Run flet."""

    def update_text(new_text: str) -> None:
        text_field.value = new_text
        page.update()

    def on_code_change(event: Any = None) -> None:
        reload(src.rules)
        code = (event.control.value.strip() if event else "") or "None"

        try:
            re = src.rules.RuleEvaluator(code)
            rules = "\n".join(
                f"{rule.ok} Rule {i}: {rule.text}"
                for i, rule in enumerate(re.rules, start=1)
            )
            update_text(
                f"""{rules}

Your expression evaluates to: {re.result}

{re.symbols}

{json.dumps(re.ast, indent=2)}"""
            )
        except Exception as e:  # noqa: BLE001
            update_text(repr(e))

    page.title = title
    page.scroll = "adaptive"  # type: ignore

    code_field = ft.TextField(label="python", on_change=on_code_change)
    text_field = ft.Text()

    page.add(ft.Text(title), code_field, text_field)
    on_code_change()


if __name__ == "__main__":
    ft.app(port=51111, target=main, view=ft.AppView.WEB_BROWSER)

"""Code game."""
import json
import os
from typing import Any

import flet as ft

from src.rules import RuleEvaluator

title = "the eval game"
width = 500
debug = bool(os.environ.get("DEBUG"))


def main(page: ft.Page) -> None:
    """Run flet."""
    page.title = title
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    best_i = 0

    def update_rule_list(re: RuleEvaluator) -> None:
        for i, rule in enumerate(re.rules):  # noqa: B007
            if not rule.ok:
                break

        nonlocal best_i
        best_i = max(best_i, i)  # type: ignore

        rule_list.controls = [
            ft.Container(
                content=ft.Text(
                    f"{'✔' if rule.ok else '✖'} Rule {i+1}: {rule.text}",
                    size=20,
                    color=ft.colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                bgcolor=ft.colors.GREEN if rule.ok else ft.colors.RED,
                padding=5,
                width=width,
            )
            for i, rule in reversed(list(enumerate(re.rules[: best_i + 1])))
        ]

        if all(rule.ok for rule in re.rules):
            rule_list.controls = [
                ft.Container(
                    content=ft.Text(
                        (
                            f"Your solution is {len(re.code)} characters,"
                            " add it to the leaderboard!"
                        ),
                        size=20,
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    bgcolor=ft.colors.GREEN,
                    padding=5,
                    width=width,
                )
            ]
        page.update()

    def update_text(new_text: str) -> None:
        text_field.value = new_text
        page.update()

    def on_code_change(event: Any = None) -> None:
        code = (event.control.value.strip() if event else "") or "None"

        try:
            re = RuleEvaluator(code)
            update_rule_list(re)
            text_content = [f"Your expression evaluates to: {re.result}"]
            if debug:
                text_content.append(
                    "\n".join(f"{rule.ok} {rule.text}" for rule in re.rules)
                )
                text_content.append(
                    str({k: v for k, v in re.symbols.items() if k != "__builtins__"})
                )
                text_content.append(json.dumps(re.ast, indent=2))
            update_text("\n\n".join(text_content))
        except Exception as e:  # noqa: BLE001
            update_text(repr(e))

    code_field = ft.TextField(
        label="python", autocorrect=False, on_change=on_code_change
    )
    text_field = ft.Text()
    rule_list = ft.Column(controls=[])
    leaderboard = ft.Markdown(
        "[leaderboard](https://docs.google.com/spreadsheets/d/1ple0iI5pmSDbpPTNZEv6Hbyq5zgAgfp3FLxPJm5ajVc/edit?usp=drivesdk)",
        on_tap_link=lambda e: page.launch_url(e.data),
    )
    layout = ft.Column(
        controls=[ft.Text(title), leaderboard, code_field, text_field, rule_list],
        width=width,
    )
    page.add(layout)
    on_code_change()


ft.app(port=51111, target=main, view=ft.AppView.WEB_BROWSER)

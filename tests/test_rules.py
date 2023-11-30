"""Tests."""

import pytest

from src.rules import RuleEvaluator


@pytest.mark.parametrize("code", ["1"])
def test_rule_evaluator_smoke_test(code: str) -> None:
    # Act
    RuleEvaluator(code)


def test_rule_evaluator_creates_password_file() -> None:
    # Arrange
    from pathlib import Path

    # Assuming this script is located inside the target directory
    password_file = Path(__file__).parent.parent / "password.txt"
    password_file.unlink(missing_ok=True)
    assert not password_file.exists()

    # Act
    RuleEvaluator("1")

    # Assert
    assert password_file.exists()


@pytest.mark.parametrize(
    ("code", "expected_ok"), [("1", False), ('(C := type("C", (object,), {}))', True)]
)
def test_rule_class(code: str, expected_ok: bool) -> None:
    # Act
    ok = RuleEvaluator(code).rule_class()

    # Assert
    assert ok == expected_ok


@pytest.mark.parametrize(
    ("code", "expected_ok"),
    [
        ("print()", True),
        ("(print := 1,).__getitem__(0)", False),
        ("print.__dir__()", False),
    ],
)
def test_rule_print(code: str, expected_ok: bool) -> None:
    # Act
    ok = RuleEvaluator(code).rule_print()

    # Assert
    assert ok == expected_ok

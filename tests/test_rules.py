"""Tests."""
import pytest

from src.rules import RuleEvaluator


@pytest.mark.parametrize("code", ["1"])
def test_evaluate_rules_smoke_test(code: str) -> None:
    # Act
    RuleEvaluator(code)


@pytest.mark.parametrize(
    ("code", "expected_ok"), [("1", False), ('(C := type("C", (object,), {}))', True)]
)
def test_rule_class(code: str, expected_ok: bool) -> None:
    # Act
    ok = RuleEvaluator(code).rule_class()

    # Assert
    assert ok == expected_ok

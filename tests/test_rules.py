"""Tests."""
import pytest

from src.rules import evaluate_rules


@pytest.mark.parametrize("code", ["1"])
def test_evaluate_rules_smoke_test(code: str) -> None:
    # Act
    evaluate_rules(code)

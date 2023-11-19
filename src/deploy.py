"""Deploys code."""
from dataclasses import dataclass


@dataclass
class Response:
    """A response."""

    ok: bool


def deploy() -> Response:
    """Deploys code."""
    return Response(ok=True)

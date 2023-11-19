"""CLI entry point."""
import typer

from src.deploy import Response, deploy


def main() -> Response:
    """CLI entry point."""
    return deploy()


if __name__ == "__main__":
    typer.run(main)

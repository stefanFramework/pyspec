from __future__ import annotations

import typer

from pyspec.sources.base import Ticket


class ManualSource:
    """No-integration source: asks for the ticket's title and description on the console."""

    def fetch(self, ticket_id: str) -> Ticket:
        title = typer.prompt(f"Title for ticket {ticket_id}")
        typer.echo("Ticket description (empty line to finish):")
        lines: list[str] = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        return Ticket(id=ticket_id, title=title, description="\n".join(lines))
